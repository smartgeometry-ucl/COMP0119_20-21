//
// COMPM080 - example by YS
//
#include <igl/readOFF.h>
#include <igl/readOBJ.h>
#include <igl/opengl/glfw/Viewer.h>
#include <igl/opengl/glfw/imgui/ImGuiMenu.h>
#include <igl/opengl/glfw/imgui/ImGuiHelpers.h>
#include <igl/vertex_triangle_adjacency.h>
#include <imgui/imgui.h>
#include <iostream>

// Create a context object 
class MyContext
{
public:
    //magic Eigen3 macro : https://eigen.tuxfamily.org/dox/group__TopicStructHavingEigenMembers.html
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    
    // vertices n,3
    Eigen::MatrixXd V;
    // vertices normals 
    Eigen::MatrixXd VN;
    
    // faces k,2 
    Eigen::MatrixXi F;
    // face normals k,3 
    Eigen::MatrixXd FN;
    
    std::vector<std::vector<int> > VF;
    std::vector<std::vector<int> > VFi;
    
    // GUI states 
    int    num_vex;
    float  nv_len;
    float  point_size;
    float  line_width;
    int    sel_vidx;
    int    mode;

	bool show_mesh;
	bool show_normals;
};

MyContext g_myctx;


void initial_context(MyContext & ctx , Eigen::MatrixXd const V, Eigen::MatrixXi const F )
{   
    ctx.point_size = 5;
    ctx.nv_len = 0.01;
    ctx.line_width = 1;
    ctx.sel_vidx = 0;
    ctx.mode = 0;
    ctx.show_normals=0;
	ctx.show_mesh=0;

	ctx.V = V;
	ctx.F = F;

    ctx.num_vex = ctx.V.rows();

    // calculate normal
    igl::per_vertex_normals(ctx.V, ctx.F, ctx.VN);

    // build adjacent matrix  
    igl::vertex_triangle_adjacency( ctx.V.rows(), ctx.F, ctx.VF, ctx.VFi);
    
} 


void add_points(igl::opengl::glfw::Viewer& viewer, Eigen::MatrixXd const  & pts_n3, Eigen::RowVector3d const  & color )
{
    //mark points 
    viewer.data().add_points(pts_n3, color);
    
}

void add_edges(igl::opengl::glfw::Viewer& viewer, Eigen::MatrixXd const &  p0, Eigen::MatrixXd const  & p1, Eigen::MatrixXd const &  color)
{
    viewer.data().add_edges(p0, p1, color );
}

void add_mesh(igl::opengl::glfw::Viewer& viewer, Eigen::MatrixXd const &  V ,  Eigen::MatrixXi const & F)
{

	viewer.data().set_mesh(V, F);

}

void add_mesh(igl::opengl::glfw::Viewer& viewer, Eigen::MatrixXd const &  V, Eigen::MatrixXi const & F, Eigen::MatrixXd const & color)
{
	// color  #V|#F|1 by 3 list of colors

	viewer.data().set_mesh(V, F);
	viewer.data().set_colors(color);

}

void reset_display(igl::opengl::glfw::Viewer& viewer, MyContext & ctx )
{
    
    viewer.data().clear();

	//======================================================================
	// add mesh 
	if(ctx.show_mesh){
		Eigen::RowVector3d mesh_color;
		mesh_color << 0.0, 1.0, 0.0;

		add_mesh(viewer, ctx.V, ctx.F, mesh_color);
		viewer.core().align_camera_center(ctx.V, ctx.F);

	}

	//======================================================================
    // hide default wireframe
    viewer.data().show_lines = 1;
    //viewer.data().show_overlay_depth = 1;
    //viewer.data().show_faces = 1;

    //======================================================================
    // visualize adjacent vertices
    {
        Eigen::MatrixXd adj_vex;
        adj_vex.resize(ctx.VF[ctx.sel_vidx].size() * 2, 3);

        int count = 0;
        // get adjacent faces & vertices
        for (size_t i = 0; i < ctx.VF[ctx.sel_vidx].size(); i++)
        {
            int face_idx = ctx.VF[ctx.sel_vidx][i];
            int v_local_idx = ctx.VFi[ctx.sel_vidx][i];

            for (int iv = 0; iv < 3; iv++)
            {
                if (iv != v_local_idx)
                {
                    Eigen::RowVector3d const vex = ctx.V.row(ctx.F(face_idx, iv));
                    adj_vex.row(count) = vex;
                    count++;
                }
            }
        } 
        
        //add  points
        add_points(viewer,  ctx.V.row(ctx.sel_vidx) , Eigen::RowVector3d(1, 0, 0) );
        
        add_points(viewer,  adj_vex , Eigen::RowVector3d(1, 0, 0) );
        
        // add links
        Eigen::MatrixXd EV1 = adj_vex;
        Eigen::MatrixXd EV2(adj_vex.rows(), 3);
        EV2.setZero();
        EV2 = EV2.rowwise() + ctx.V.row(ctx.sel_vidx);

        add_edges(viewer, EV1, EV2, Eigen::RowVector3d(1, 0, 0));

		if(!ctx.show_mesh && !ctx.show_normals){
			viewer.core().align_camera_center(EV1);
		}
    } 
    
    //======================================================================
    // add normal lines
	if(ctx.show_normals)
    {
        Eigen::MatrixXd EV1(ctx.V);
        Eigen::MatrixXd EV2;
        
        // show real VN
        EV2 = EV1 + ctx.VN * ctx.nv_len;

        add_edges(viewer,EV1, EV2, Eigen::RowVector3d(1, 1, 1));   
		viewer.core().align_camera_center(ctx.V, ctx.F);
    }


    //======================================================================

    viewer.data().line_width = ctx.line_width;
    viewer.data().point_size = ctx.point_size;

}


bool key_down(igl::opengl::glfw::Viewer& viewer, unsigned char key, int modifier)
{

    std::cout << "Key: " << key << " " << (unsigned int)key << std::endl;
    if (key=='q' || key=='Q')
    {
        exit(0);
    }
    return false;
}


void initial_viewer(igl::opengl::glfw::Viewer& viewer , igl::opengl::glfw::imgui::ImGuiMenu & menu)
{
    // Add additional windows via defining a Lambda expression with captures by reference([&])
    menu.callback_draw_custom_window = [&]()
    {   
        bool require_reset=false;
    
        // Define next window position + size
        ImGui::SetNextWindowPos(ImVec2(180.f * menu.menu_scaling(), 10), ImGuiSetCond_FirstUseEver);
        ImGui::SetNextWindowSize(ImVec2(300, 160), ImGuiSetCond_FirstUseEver);
        ImGui::Begin( "MyProperties", nullptr, ImGuiWindowFlags_NoSavedSettings );
        
        // point size
        // [event handle] if value changed
        if (ImGui::InputFloat("point_size", &g_myctx.point_size))
        {
            std::cout << "point_size changed\n";
            viewer.data().point_size = g_myctx.point_size;
        }

        // line width
        // [event handle] if value changed
        if(ImGui::InputFloat("line_width", &g_myctx.line_width))
        {
            std::cout << "line_width changed\n";
            viewer.data().line_width = g_myctx.line_width;
        }

        // length of normal line
        // [event handle] if value changed
        //if (ImGui::InputFloat("nv_length", &g_myctx.nv_len))
        if (ImGui::SliderFloat("nv_length", &g_myctx.nv_len, 0, 1, "%.3f"))
        {
            require_reset=1;
        }

        // vertex index
        if (ImGui::SliderInt("sel_vex_index", &g_myctx.sel_vidx, 0, g_myctx.num_vex-1))
        {
            require_reset=1;
        } 

		if (ImGui::Checkbox("show_mesh", &g_myctx.show_mesh))
		{
			require_reset = 1;
		}

		if (ImGui::Checkbox("show_normal", &g_myctx.show_normals))
		{
			require_reset = 1;
		}

        //mode
        if (ImGui::SliderInt("mode", &g_myctx.mode, 0, 1))
        {
            require_reset=1;
        }

        if(require_reset)
        {
            reset_display(viewer, g_myctx);
        }

        ImGui::End();
    };


    // registered a event handler
    viewer.callback_key_down = &key_down;
}


int main(int argc, char *argv[])
{   
	std::vector<std::string> buuny_path_cands{
		"../../../../../../../resources/bun_zipper_res3.obj",
		"../../../../../../resources/bun_zipper_res3.obj",
		"../../../../../resources/bun_zipper_res3.obj",
		"../../../../resources/bun_zipper_res3.obj",
		"../../../resources/bun_zipper_res3.obj",
		"../../resources/bun_zipper_res3.obj",
	};
    
	// load mesh 
	Eigen::MatrixXd V;
	Eigen::MatrixXi F;

	// brute force load 
	for( const auto fp : buuny_path_cands ){
		if (igl::readOBJ(fp, V, F)) {
			std::cout<<"load mesh at:"<<fp<<std::endl;
			break;
		}
	}

	//initial vertices and faces
    initial_context(g_myctx, V, F );
    
    
    // initial a viewer
	igl::opengl::glfw::Viewer viewer;

	// Attach a default menu plugin
	igl::opengl::glfw::imgui::ImGuiMenu menu;
	viewer.plugins.push_back(&menu);

	menu.callback_draw_viewer_menu = [&]()
	{
		menu.draw_viewer_menu();
	};

	// Add our GUI items
    initial_viewer(viewer, menu);
    
    // set up initial display 
    reset_display(viewer, g_myctx);

    // Call GUI
    viewer.launch();

}

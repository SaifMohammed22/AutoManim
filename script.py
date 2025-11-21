from manim import *

class CustomScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Define the grid
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10
        )
        grid.set(stroke_color=WHITE, stroke_width=0.5)

        # Define the vector
        vector = Arrow(
            start=np.array([0, 0, 0]),
            end=np.array([2, 1, 0]),
            buff=0
        )
        vector.set(fill_color=YELLOW, stroke_color=YELLOW)

        # Define the transformation matrix
        matrix = [[1, 1], [0, 1]]  # Shear transformation

        # Create the transformed vector
        transformed_vector_end = np.array([
            matrix[0][0] * 2 + matrix[0][1] * 1,
            matrix[1][0] * 2 + matrix[1][1] * 1,
            0
        ])
        transformed_vector = Arrow(
            start=np.array([0, 0, 0]),
            end=transformed_vector_end,
            buff=0
        )
        transformed_vector.set(fill_color=RED, stroke_color=RED)

        # Create the transformed grid
        transformed_grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10
        )

        for i in range(-5,6):
            for j in range(-5,6):
                original_point = np.array([i, j, 0])
                transformed_point = np.array([
                    matrix[0][0] * i + matrix[0][1] * j,
                    matrix[1][0] * i + matrix[1][1] * j,
                    0
                ])
                transformed_grid.coords_to_point(i,j)
                transformed_grid.coords_to_point(transformed_point[0], transformed_point[1])

        transformed_grid.set(stroke_color=BLUE, stroke_width=0.5)


        # Show the original grid and vector
        self.play(Create(grid))
        self.play(Create(vector))
        self.wait(1)

        # Transform the grid and vector
        self.play(
            ReplacementTransform(grid.copy(), transformed_grid),
            ReplacementTransform(vector.copy(), transformed_vector)
        )
        self.wait(1)

        # Display the transformation matrix
        matrix_text = MathTex(
            "\\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}"
        )
        matrix_text.move_to(np.array([3, 3, 0]))
        matrix_text.set(fill_color=GREEN)

        self.play(FadeIn(matrix_text))
        self.wait(3)

        # Show the effect of the transformation
        text1 = Tex("Shear Transformation", color=ORANGE)
        text1.move_to(np.array([0, 3.5, 0]))
        self.play(FadeIn(text1))
        self.wait(3)

        text2 = MathTex("\\vec{v} = \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}")
        text2.move_to(np.array([3,-3,0]))
        text2.set(fill_color=YELLOW)
        self.play(FadeIn(text2))
        self.wait(2)

        text3 = MathTex("A\\vec{v} = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix} \\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix} = \\begin{bmatrix} 3 \\\\ 1 \\end{bmatrix}")
        text3.move_to(np.array([-3,-3,0]))
        text3.set(fill_color=RED)
        self.play(FadeIn(text3))
        self.wait(3)

        # Clean up
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3), FadeOut(matrix_text))
        self.wait(1)

        self.wait(1)
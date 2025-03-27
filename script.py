
from manim import *

class CustomScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # Define the axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"stroke_color": WHITE}
        )
        self.add(axes)

        # Define a vector
        vector = Arrow(
            start=np.array([0, 0, 0]),
            end=np.array([2, 1, 0]),
            buff=0,
            color=YELLOW
        )
        self.add(vector)

        # Define the transformation matrix
        matrix = Matrix([
            [2, 1],
            [1, 1]
        ])

        # Display the matrix
        matrix_tex = MathTex("\\begin{bmatrix} 2 & 1 \\\\ 1 & 1 \\end{bmatrix}")
        matrix_tex.move_to(np.array([3, 3, 0]))
        matrix_tex.set(fill_color=WHITE, stroke_color=WHITE)
        self.add(matrix_tex)

        # Display the vector as coordinates
        vector_coords = MathTex("\\begin{bmatrix} 2 \\\\ 1 \\end{bmatrix}")
        vector_coords.move_to(np.array([3, 1, 0]))
        vector_coords.set(fill_color=WHITE, stroke_color=WHITE)
        self.add(vector_coords)

        self.wait(2)

        # Calculate the transformed vector
        transformed_vector_coords = np.array([2*2 + 1*1, 1*2 + 1*1, 0])
        transformed_vector_coords_tex = MathTex("\\begin{bmatrix} 5 \\\\ 3 \\end{bmatrix}")
        transformed_vector_coords_tex.move_to(np.array([3, -1, 0]))
        transformed_vector_coords_tex.set(fill_color=WHITE, stroke_color=WHITE)
        self.add(transformed_vector_coords_tex)

        # Create the transformed vector
        transformed_vector = Arrow(
            start=np.array([0, 0, 0]),
            end=np.array([5, 3, 0]),
            buff=0,
            color=RED
        )

        # Animation
        self.play(Create(transformed_vector))
        self.wait(1)
        self.play(FadeOut(vector))
        self.wait(2)

        # Show grid lines
        grid = NumberPlane()
        grid.set(fill_color=WHITE, stroke_color=BLUE)
        self.play(FadeIn(grid))
        self.wait(2)
        self.play(FadeOut(grid))
        self.wait(2)
        
        # Scaling explanation
        scaling_text = MathTex("Scaling \\& Shearing")
        scaling_text.move_to(np.array([0, 3, 0]))
        scaling_text.set(fill_color=WHITE, stroke_color=WHITE)
        self.play(Create(scaling_text))
        self.wait(3)
        self.play(FadeOut(scaling_text))

        # Explain linear transformation
        linear_transformation_text = MathTex("Linear \\, Transformation")
        linear_transformation_text.move_to(np.array([0, 3, 0]))
        linear_transformation_text.set(fill_color=WHITE, stroke_color=WHITE)
        self.play(Create(linear_transformation_text))
        self.wait(3)
        self.play(FadeOut(linear_transformation_text))

        self.wait(1)

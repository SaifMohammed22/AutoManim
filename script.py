from manim import *

class CustomScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        circle = Circle(radius=2, color=WHITE)
        self.play(Create(circle))
        self.wait(1)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_axis_config={"numbers_to_include": [-2, -1, 1, 2]},
            y_axis_config={"numbers_to_include": [-2, -1, 1, 2]},
        )
        self.play(FadeIn(axes))
        self.wait(1)

        radius = Line(np.array([0, 0, 0]), np.array([2, 0, 0]), color=YELLOW)
        radius_label = MathTex("r", color=YELLOW).move_to(radius.get_center() + np.array([0.3, 0, 0]))
        self.play(Create(radius), FadeIn(radius_label))
        self.wait(1)

        dot = Dot(np.array([2, 0, 0]), color=RED)
        self.play(Create(dot))
        self.wait(1)

        angle = Arc(radius=2, start_angle=0, angle=PI/4, color=GREEN)
        angle_label = MathTex("\\theta", color=GREEN).move_to(angle.point_from_proportion(0.5) + np.array([0.3, 0.2, 0]))
        self.play(Create(angle), FadeIn(angle_label))
        self.wait(1)

        new_x = 2 * np.cos(PI/4)
        new_y = 2 * np.sin(PI/4)

        new_dot = Dot(np.array([new_x, new_y, 0]), color=RED)
        new_radius = Line(np.array([0, 0, 0]), np.array([new_x, new_y, 0]), color=YELLOW)

        self.play(ReplacementTransform(dot.copy(), new_dot), ReplacementTransform(radius.copy(), new_radius))
        self.wait(1)

        x_line = Line(np.array([new_x, new_y, 0]), np.array([new_x, 0, 0]), color=BLUE)
        y_line = Line(np.array([new_x, new_y, 0]), np.array([0, new_y, 0]), color=BLUE)

        x_label = MathTex("x", color=BLUE).next_to(x_line, np.array([0, -1, 0]))
        y_label = MathTex("y", color=BLUE).next_to(y_line, np.array([-1, 0, 0]))

        self.play(Create(x_line), Create(y_line), FadeIn(x_label), FadeIn(y_label))
        self.wait(1)

        cosine_eq = MathTex("\\cos(\\theta) = \\frac{x}{r}", color=BLUE).to_corner(np.array([1, 1, 0]))
        sine_eq = MathTex("\\sin(\\theta) = \\frac{y}{r}", color=BLUE).next_to(cosine_eq, np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]))

        self.play(FadeIn(cosine_eq), FadeIn(sine_eq))
        self.wait(1)

        group = VGroup(circle, axes, new_radius, new_dot, angle, angle_label, x_line, y_line, x_label, y_label, cosine_eq, sine_eq, radius_label)

        self.play(group.animate.scale(0.5).move_to(np.array([0, 0, 0])))
        self.wait(1)

        for i in range(4):
            theta_val = i * PI/4
            new_x_i = 2 * np.cos(theta_val)
            new_y_i = 2 * np.sin(theta_val)

            new_dot_i = Dot(np.array([new_x_i, new_y_i, 0]), color=RED)
            new_radius_i = Line(np.array([0, 0, 0]), np.array([new_x_i, new_y_i, 0]), color=YELLOW)
            angle_i = Arc(radius=2, start_angle=0, angle=theta_val, color=GREEN)

            self.play(ReplacementTransform(new_dot.copy(), new_dot_i), ReplacementTransform(new_radius.copy(), new_radius_i), ReplacementTransform(angle.copy(), angle_i))
            new_dot = new_dot_i
            new_radius = new_radius_i
            angle = angle_i

            x_line_i = Line(np.array([new_x_i, new_y_i, 0]), np.array([new_x_i, 0, 0]), color=BLUE)
            y_line_i = Line(np.array([new_x_i, new_y_i, 0]), np.array([0, new_y_i, 0]), color=BLUE)
            self.play(ReplacementTransform(x_line.copy(), x_line_i), ReplacementTransform(y_line.copy(), y_line_i))
            x_line = x_line_i
            y_line = y_line_i
            self.wait(1)

        self.wait(1)
import subprocess
import gradio as gr
import google.generativeai as genai
import os
import re

# Set up API key
API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise ValueError("Please set the GENAI_API_KEY environment variable.")

genai.configure(api_key=API_KEY)

def generate_manim_code(prompt):
    """Uses Google GenAI to generate a Manim script from a given prompt."""
    system_prompt = (
            """**Manim Code Generator (v0.19.0)**

Generate a complete, executable Python script for Manim v0.19.0 that accurately visualizes a mathematical concept. The animation should last at least 25 seconds and be mathematically correct, with clear visual aids.

STRUCTURAL REQUIREMENTS:
- Import exactly: `from manim import *`
- Define the scene as: `class CustomScene(Scene):`
- In the `construct()` method, the first line must be: `self.camera.background_color = BLACK`
- The last line must be: `self.wait(1)`

SYNTAX RULES:
- Use only `np.array([x, y, 0])` for all positioning.
- For styling, use only: `obj.set(fill_color=COLOR, stroke_color=COLOR)`
- Allowed colors: `WHITE`, `BLACK`, `RED`, `BLUE`, `GREEN`, `YELLOW`, `ORANGE`, `PURPLE`
- All LaTeX must use double backslashes (e.g., `MathTex("\\frac{x}{y}")`)
- Use only documented parameters for Manim v0.19.0

AVOID THESE (CRITICAL FOR DOCKER COMPATIBILITY AND ERROR-FREE CODE):
- Do NOT use: `set_fill()`, `set_stroke()`, `set_color()`, the `.animate` method, or `ApplyMethod`
- Do NOT use: constants like `RIGHT`, `LEFT`, `UP`, `DOWN` (use arrays instead)
- Do NOT use: `ValueTracker`, `UpdateFromFunc`, or any custom updaters
- Do NOT transform objects after modifying them
- Do NOT include custom fonts, images, or external assets
- Do NOT perform file operations or use external dependencies
- Do NOT use parameters that cause errors (e.g., `axis_tip_length` in Axes)

ANIMATION GUIDELINES:
- Use animation methods: `Create()`, `FadeIn()`, `FadeOut()`, and `ReplacementTransform()`
- Always add `self.wait(1)` after a sequence of animations
- Always create copies of objects (using `.copy()`) before transforming them
- Create new objects for any transformed state instead of modifying an existing object

TECHNICAL REQUIREMENTS:
- Define all objects before using them in animations
- Use `self.add()` to add objects to the scene
- Use `NumberPlane()` for grids with default parameters
- Limit animations to a maximum of 10 in a row before inserting a `self.wait()`
- Use `Axes()` only with basic parameters (e.g., x_range, y_range, axis_config)
- Ensure that every mobject exists before it is animated

MATHEMATICAL ACCURACY:
- Prioritize correct math with accurate formulas and clear, readable equations
- Include appropriate visual aids to enhance understanding of the mathematical concept

OUTPUT:
- Return only raw Python code (no markdown or explanations)
- The code must be complete, executable, simple, and readable
- Ensure the animation runs for a minimum of 25 seconds by using strategic `self.wait()` pauses

CHAIN OF THOUGHT:
1. Create the basic scene structure with the required import and class.
2. Define all necessary mobjects with precise positions using `np.array([x, y, 0])` and proper styling.
3. Sequence animations logically using the allowed methods and ensure strategic pauses.
4. Validate all mathematical formulas and visual aids for correctness.
5. Double-check that all syntax rules are followed and banned methods are avoided.
6. Return only the complete raw Python code.
"""
    )

    full_prompt = system_prompt + prompt

    # Generate content using Gemini API
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(full_prompt)

    # Extract generated code safely
    manim_code = response.text if hasattr(response, 'text') else str(response)
    manim_code = clearn_manim_code(manim_code)

    # Save script for debugging
    script_path = "script.py"
    with open(script_path, "w") as f:
        f.write(manim_code)

    print(f"Manim script saved at: {script_path}")
    return script_path  # Return path for checking

def clearn_manim_code(code):
    # Replace fancy quotes with standard ones and remove markdown formatting
    code = code.replace("“", '"').replace("”", '"')  
    code = code.replace("‘", "'").replace("’", "'")
    code = code.replace("```python", "").replace("```", "")
    # Remove non-ASCII characters that might cause syntax errors
    code = re.sub(r'[^\x00-\x7F]+', '', code)
    return code


def render_manim(prompt):
    """Generates and renders a Manim animation using Docker."""
    try:
        script_path = generate_manim_code(prompt)

        # Run Manim inside Docker
        result = subprocess.run([ "sudo", "groupadd docker", "sudo","usermod", "-aG", "docker"
         "$USER", "newgrp", "docker"], shell=True, capture_output=True, text=True)
        result = subprocess.run([
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/manim",
            "manimcommunity/manim",
            "manim", "/manim/script.py", "-ql"
        ], capture_output=True, text=True)

        # Write Docker logs to a file for debugging
        with open("docker_debug.log", "w") as log_file:
            log_file.write("STDOUT:\n" + result.stdout + "\n")
            log_file.write("STDERR:\n" + result.stderr + "\n")

        print("Docker STDOUT:", result.stdout)
        print("Docker STDERR:", result.stderr)

        # Check for output videos (update path if necessary)
        output_dir = os.path.join(os.getcwd(), "media/videos/script/480p15")
        if not os.path.exists(output_dir):
            print(f"Output directory does not exist: {output_dir}")
            return f"Error: Output directory {output_dir} not found."

        output_files = [f for f in os.listdir(output_dir) if f.endswith(".mp4")]
        print(output_files)
        if output_files:
            video_path = os.path.join(output_dir, output_files[0])
            output_files.pop(0)
            print(f"Video found: {video_path}")
            return video_path
        else:
            print("Error: No output video found.")
            return "Error: No output video found. Check logs above."

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return f"Error: {str(e)}"



# Gradio interface
inf = gr.Interface(
    fn=render_manim,
    inputs=gr.Textbox(label="Describe the mathematical concept to animate"),
    outputs=gr.Video(label="Generated Animation"),
    title="Manim Animation Generator"
)

if __name__ == "__main__":
    inf.launch()
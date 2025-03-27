import subprocess
import gradio as gr
import os
import re
from openai import OpenAI

DEEPSEEK_API = os.getenv("DEEPSEEK_API")

if not DEEPSEEK_API:
    raise ValueError("Please set the DEEPSEEK_API environment variable.")

def generate_manim_code(prompt):
    system_prompt = (
"""You are an Expert Manim Developer. Your task is to generate complete, executable Python scripts using Manim v0.19 that visualize mathematical concepts with effective animations.

## 🔹 **Output Rules**
- Return ONLY raw Python code without markdown or explanations
- Use modern Manim v0.19 syntax with proper imports and Scene class structure
- Ensure full code structure: imports, Scene subclass, construct() method
- Validate code for syntax errors and runtime execution
- Prioritize simplicity and readability
- Use Tex/MathTex for equations instead of Text
- Include proper scene setup and object positioning
- Maintain consistent code formatting and indentation
- Make the animation visually appealing and informative
- the video should be not less that 25 seconds

## 🔹 **Animation Guidelines**
- Animate equations with Write() and FadeOut()
- Apply rate_func=smooth for natural movement
- Highlight key elements with SurroundingRectangle or Underline
- Use VGroup for logical object grouping
- Include proper positioning (.shift(), .next_to())
- Maintain clear scene flow with self.play() sequencing

## 🔹 **Technical Requirements**
- Mandatory imports: from manim import *
- Required scene structure:
class CustomScene(Scene):
    def construct(self):
        # Animation code
- Include appropriate animation timing (run_time)
- Use black color scheme unless specified otherwise
- Ensure mobject proper anchoring and scaling"""
    )

    

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=DEEPSEEK_API
    )
    
    completion = client.chat.completions.create(
        model = "deepseek/deepseek-r1:free",
        messages=[
            {
                "role" : "user",
                "content" : system_prompt
            }
        ]
    )

    manim_code = completion.choices[0].message.content
    manim_code = clearn_manim_code(manim_code)

    print(manim_code)
    script_path = 'script.py'
    with open(script_path, 'w') as f:
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

!pip install -q gradio

import os
import re
import tempfile
import gradio as gr


def show_form():
    return gr.update(visible=False), gr.update(visible=True)


def generate_readme(project_name, description, technologies, features, installation):
    project_name = (project_name or "").strip()
    description = (description or "").strip()
    technologies = technologies or ""
    features = features or ""
    installation = (installation or "").strip()

    if not project_name:
        return (
            gr.update(),
            gr.update(),
            gr.update(),
            "⚠️ Please enter your project name.",
            gr.update(visible=True),
            gr.update(visible=False),
        )

    if not description:
        return (
            gr.update(),
            gr.update(),
            gr.update(),
            "⚠️ Please enter your project description.",
            gr.update(visible=True),
            gr.update(visible=False),
        )

    tech_items = [item.strip() for item in technologies.split(",") if item.strip()]
    feature_items = [item.strip() for item in features.splitlines() if item.strip()]

    tech_text = "\n".join(f"- {item}" for item in tech_items) or "- Not specified"
    feature_text = "\n".join(f"- {item}" for item in feature_items) or "- Not specified"
    install_text = installation or "Installation instructions not provided."

    readme_text = f"""# {project_name}

## About the Project

{description}

## Technologies Used

{tech_text}

## Features

{feature_text}

## Installation

```bash
{install_text}
```

## Author

Created using Smart GitHub README Generator.

---
If you like this project, don't forget to give it a star!
"""

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", project_name).strip("_") or "project"
    output_path = os.path.join(tempfile.gettempdir(), f"{safe_name}_README.md")

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(readme_text)

    return (
        readme_text,
        output_path,
        "✅ Your README has been generated successfully!",
        "",
        gr.update(visible=False),
        gr.update(visible=True),
    )


def edit_details():
    return gr.update(visible=True), gr.update(visible=False)


def start_over():
    return (
        gr.update(visible=True),
        gr.update(visible=False),
        "",
        "",
        "",
        "",
        "",
        "Your README preview will appear here.",
        None,
        "Enter your project details to get started.",
        "",
    )


custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff, #eff6ff);
    font-family: Arial, sans-serif;
}
#hero {
    background: linear-gradient(120deg, #4338ca, #9333ea, #2563eb);
    padding: 48px 28px;
    border-radius: 22px;
    text-align: center;
    color: white;
    margin: 25px auto;
    max-width: 1000px;
}
#hero h1, #hero h2, #hero p {
    color: white !important;
}
#hero h1 {
    font-size: 38px;
    margin-bottom: 12px;
}
#hero .quote {
    font-size: 19px;
    margin-top: 20px;
    font-style: italic;
}
.page-panel {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 24px;
}
.generate-button, .next-button {
    background: linear-gradient(90deg, #4f46e5, #9333ea) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    min-height: 48px;
}
.secondary-button {
    border-radius: 12px !important;
    min-height: 44px;
}

/* ---------- Download panel (page 3) ---------- */
.download-panel {
    background: #f5f3ff !important;
    border: 2px solid #c4b5fd !important;
    border-radius: 22px !important;
    padding: 0 !important;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(124, 58, 237, 0.22);
}
.download-banner {
    background: #7c3aed;
    padding: 24px 20px;
    text-align: center;
    color: white;
}
.download-banner h3 {
    margin: 8px 0 4px 0;
    font-size: 24px;
    color: white !important;
}
.download-banner p {
    margin: 0;
    font-size: 15px;
    color: white !important;
    opacity: 0.95;
}
.download-body {
    padding: 20px 22px 22px 22px;
}
#download-file {
    background: rgba(255, 255, 255, 0.85) !important;
    border: 2px dashed #8b5cf6 !important;
    border-radius: 16px !important;
}
#download-file a {
    color: #7c3aed !important;
    font-weight: bold !important;
}
#download-file button, #download-file .download-link {
    color: #7c3aed !important;
}
/* ---------- Hide Gradio footer (Built with Gradio, Use via API, Settings) ---------- */
footer, .footer, .show-api, .built-with, .settings {
    display: none !important;
}

/* ---------- Solid black text on page 3 (no faded words) ---------- */
.dark-text, .dark-text * {
    color: #000000 !important;
    opacity: 1 !important;
}
.page-panel :is(p, li, h1, h2, h3, h4, h5, h6, strong, em, blockquote, td, th, span.md) {
    color: #000000 !important;
    opacity: 1 !important;
}
.page-panel .prose, .page-panel .prose * {
    opacity: 1 !important;
}
"""


# Gradio 6 moved theme and css from gr.Blocks() to demo.launch().
# This works on both older and newer versions.
GRADIO_MAJOR = int(gr.__version__.split(".")[0])
app_theme = gr.themes.Soft(primary_hue="violet", secondary_hue="blue")

blocks_kwargs = {"title": "Smart GitHub README Generator"}
if GRADIO_MAJOR < 6:
    blocks_kwargs["theme"] = app_theme
    blocks_kwargs["css"] = custom_css

with gr.Blocks(**blocks_kwargs) as demo:

    # PAGE 1: Welcome screen
    with gr.Column(visible=True) as welcome_page:
        gr.HTML("""
        <div id="hero">
            <h1>🚀 Smart GitHub README Generator</h1>
            <p>Create beautiful and professional GitHub README files in seconds.</p>
            <p class="quote">“Every great project deserves a README that tells its story.”</p>
        </div>
        """)
        gr.Markdown(
            "### Turn your project details into a clear, professional README."
        )
        gr.Markdown(
            "No need to write the Markdown from scratch. Enter your project "
            "information, generate the README, preview it, and download it."
        )
        next_button = gr.Button(
            "Get Started  →",
            variant="primary",
            elem_classes=["next-button"]
        )

    # PAGE 2: Project information form
    with gr.Column(visible=False) as form_page:
        gr.Markdown("# 📝 Enter Your Project Details")
        gr.Markdown("Fill in the details below, then generate your README.")

        with gr.Row():
            with gr.Column(elem_classes=["page-panel"]):
                project_name = gr.Textbox(
                    label="📌 Project Name",
                    placeholder="Example: Student Management System"
                )
                description = gr.Textbox(
                    label="📖 Project Description",
                    placeholder="Describe what your project does...",
                    lines=4
                )
                technologies = gr.Textbox(
                    label="🛠️ Technologies Used",
                    placeholder="Python, Gradio, HTML, CSS"
                )
                features = gr.Textbox(
                    label="✨ Project Features",
                    placeholder="Enter one feature per line",
                    lines=5
                )
                installation = gr.Textbox(
                    label="⚙️ Installation Instructions",
                    placeholder="pip install -r requirements.txt",
                    lines=3
                )

        form_status = gr.Markdown("")
        with gr.Row():
            back_to_welcome = gr.Button(
                "← Back",
                elem_classes=["secondary-button"]
            )
            generate_button = gr.Button(
                "✨ Generate My README",
                variant="primary",
                elem_classes=["generate-button"]
            )

    # PAGE 3: Generated README and download
    with gr.Column(visible=False) as result_page:
        gr.Markdown("# Your README Is Ready!", elem_classes=["dark-text"])
        result_status = gr.Markdown("✅ Your README has been generated successfully.", elem_classes=["dark-text"])

        with gr.Row():
            with gr.Column(elem_classes=["page-panel"]):
                gr.Markdown("### README Preview")
                preview = gr.Markdown("Your README preview will appear here.")

            # Download panel
            with gr.Column(elem_classes=["download-panel"]):
                gr.HTML("""
                <div class="download-banner">
                    <h3>Download Your README</h3>
                    <p>Your README.md file is ready to grab!</p>
                </div>
                """)
                with gr.Column(elem_classes=["download-body"]):
                    download_file = gr.File(
                        label="Your README.md",
                        elem_id="download-file"
                    )
                    gr.Markdown(
                        "Click the file above to download it.",
                        elem_classes=["dark-text"]
                    )


        with gr.Row():
            edit_button = gr.Button(
                "← Edit Project Details",
                elem_classes=["secondary-button"]
            )
            new_project_button = gr.Button(
                "＋ Create Another README",
                variant="primary",
                elem_classes=["generate-button"]
            )


    next_button.click(
        fn=show_form,
        inputs=[],
        outputs=[welcome_page, form_page]
    )

    back_to_welcome.click(
        fn=lambda: (gr.update(visible=True), gr.update(visible=False)),
        inputs=[],
        outputs=[welcome_page, form_page]
    )

    generate_button.click(
        fn=generate_readme,
        inputs=[
            project_name,
            description,
            technologies,
            features,
            installation
        ],
        outputs=[
            preview,
            download_file,
            result_status,
            form_status,
            form_page,
            result_page
        ]
    )

    edit_button.click(
        fn=edit_details,
        inputs=[],
        outputs=[form_page, result_page]
    )

    new_project_button.click(
        fn=start_over,
        inputs=[],
        outputs=[
            welcome_page,
            form_page,
            project_name,
            description,
            technologies,
            features,
            installation,
            preview,
            download_file,
            result_status,
            form_status
        ]
    )

if GRADIO_MAJOR < 6:
    demo.launch(share=True, show_api=False)
else:
    demo.launch(share=True, theme=app_theme, css=custom_css)

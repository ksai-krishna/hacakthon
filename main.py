import gradio as gr #pip install gradio

def calculate_cost(file, text_input, additional_text, price_per_1000_tokens):
    try:
        # Initialize text content
        text_content = ""

        # Decode file content or use text input
        if file is not None:
            text_content = file.decode("utf-8")  # Decode the bytes object directly
        elif text_input.strip():
            text_content = text_input
        else:
            return "Please provide text or upload a file.", "0", []

        # Combine with additional text if provided
        if additional_text.strip():
            text_content += " " + additional_text

        # Tokenize text (split into words)
        tokens = text_content.split()

        # Count tokens
        token_count = len(tokens)

        # Ensure valid price per 1000 tokens
        price_per_1000_tokens = float(price_per_1000_tokens)

        # Calculate cost
        total_cost = (token_count / 1000)
        total_cost=total_cost* price_per_1000_tokens

        # Round total cost to 2 decimal places
        total_cost = round(total_cost, 4)

        # Return the results
        return f"Token Count: {token_count}", f"Total Cost: ${total_cost}", tokens

    except Exception as e:
        return f"Error: {str(e)}", "0", []

def generate_file(tokens, total_cost):
    try:
        # Generate file content with tokens and total cost
        file_content = f"Tokens:\n{' '.join(tokens)}\n\nTotal Cost: ${total_cost}"
        # Write to a temporary file
        file_path = "token_cost.txt"
        with open(file_path, "w") as file:
            file.write(file_content)
        return file_path
    except Exception as e:
        return f"Error generating file: {str(e)}"

# Define the Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown("## Token Cost Calculator")

    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload Text File (.txt)", type="binary")
            text_input = gr.Textbox(label="Enter Main Text", lines=10, placeholder="Type or paste your main text here...")
            additional_text = gr.Textbox(label="Additional Text", lines=5, placeholder="Type additional text here if needed...")
            price_input = gr.Number(label="Price per 1000 Tokens", value=0.01)

        with gr.Column():
            token_count_display = gr.Textbox(label="Token Count", interactive=False)
            total_cost_display = gr.Textbox(label="Total Cost", interactive=False)
            token_list_state = gr.State()

    with gr.Row():
        calculate_button = gr.Button("Calculate")
        download_button = gr.Button("Download Tokens and Cost")

    # Outputs for file download
    file_output = gr.File(label="Download File")

    # Define interactions
    calculate_button.click(
        calculate_cost,
        inputs=[file_input, text_input, additional_text, price_input],
        outputs=[token_count_display, total_cost_display, token_list_state]
    )

    download_button.click(
        generate_file,
        inputs=[token_list_state, total_cost_display],
        outputs=[file_output]
    )

# Launch the Gradio interface
demo.launch()

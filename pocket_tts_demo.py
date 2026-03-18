import gradio as gr
import pocket_tts
import scipy.io.wavfile
import tempfile
import numpy as np
import os

print("Loading Pocket TTS model...")
tts_model = pocket_tts.TTSModel.load_model()

VOICES = ["alba", "marius", "javert", "jean", "fantine", "cosette", "eponine", "azelma"]
voice_states = {}

print("Caching voice states...")
for voice in VOICES:
    try:
        voice_states[voice] = tts_model.get_state_for_audio_prompt(voice)
        print(f"Cached voice: {voice}")
    except Exception as e:
        print(f"Error caching voice {voice}: {e}")

def generate_speech(text, selected_voice, custom_audio):
    if not text or not text.strip():
        text = "Please provide some text to synthesize."
        
    # Determine the voice state
    if custom_audio is not None:
        # Use custom audio for voice cloning
        try:
            state = tts_model.get_state_for_audio_prompt(custom_audio)
        except Exception as e:
            print(f"Error with custom audio: {e}")
            state = voice_states.get(selected_voice, voice_states.get("alba"))
    else:
        state = voice_states.get(selected_voice, voice_states.get("alba"))
    
    # Generate audio
    audio_tensor = tts_model.generate_audio(state, text)
    audio_data = audio_tensor.cpu().numpy()
    
    # The sample rate for pocket_tts is 24000
    sample_rate = 24000
    if hasattr(tts_model, 'sample_rate'):
        sample_rate = tts_model.sample_rate
        
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    scipy.io.wavfile.write(temp_file.name, sample_rate, audio_data)
    
    return temp_file.name

with gr.Blocks(title="Pocket TTS Demo") as app:
    gr.Markdown("# Pocket TTS Demo")
    
    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="Text Input", 
                lines=4, 
                value="Hello, this is a text-to-speech demonstration using pocket TTS."
            )
            voice_dropdown = gr.Dropdown(
                label="Select Pre-built Voice", 
                choices=VOICES, 
                value="alba"
            )
            audio_upload = gr.Audio(
                label="Optional: Upload custom audio for voice cloning", 
                type="filepath", 
                sources=["upload"]
            )
            generate_btn = gr.Button("Generate Speech", variant="primary")
            
        with gr.Column(scale=1):
            audio_output = gr.Audio(label="Generated Speech Output", interactive=False)
            
    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, voice_dropdown, audio_upload],
        outputs=[audio_output]
    )

if __name__ == "__main__":
    app.launch()

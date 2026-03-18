Create a single Python file for a text-to-speech demo using Kyutai's
Pocket TTS (pocket_tts package) with a Gradio interface.

The app should:
- Load the Pocket TTS model using TTSModel.load_model()
- Offer 8 pre-built voices: alba, marius, javert, jean, fantine,
  cosette, eponine, azelma
- Cache all voice states at startup for faster generation
- Allow users to upload a custom audio file for voice cloning
- Generate speech from text input and return a .wav file
- Use scipy.io.wavfile to save the audio output

UI layout (use gr.Blocks, not gr.Interface):
- Text input box (multiline, 4 lines) with a default sample sentence
- Voice dropdown to select from pre-built voices
- Audio upload for optional custom voice cloning
- Generate Speech button (primary variant)
- Audio output player for the generated speech
- Use a two-column layout: inputs on the left (scale=2),
  output on the right (scale=1)

Use:
- pocket_tts.TTSModel for model loading and audio generation
- tts_model.get_state_for_audio_prompt() for voice state loading
- tts_model.generate_audio() for speech synthesis
- scipy.io.wavfile.write() to save audio to a temp .wav file
- tempfile.NamedTemporaryFile for temporary audio files
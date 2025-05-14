# dweller-speech

This is the official repository for the speech engine powering [Dweller](https://github.com/kannachi323/dweller). 
It includes both text-to-speech (TTS) and speech-to-text (STT) components, enabling voice interaction within the Dweller application.

## Description
Before diving into any modifications of the TTS or STT components, I recommend checking out [Dweller](https://github.com/kannachi323/dweller) to better understand its architecture and how dweller-speech fits in.

In short, Dweller is a multi-modal AI system that integrates vision, hearing, voice, and other large models to function intelligently. This repository specifically powers Dweller’s hearing and voice — enabling it to listen and speak.

The **speech-to-text** model is based on Vosk for offline, real-time transcription through an audio input (such as microphone, speakers, etc). In the [stt](https://github.com/kannachi323/dweller-speech/tree/main/stt) directory, there are a few classes that handle audio input buffering, feeding live audio data into Vosk for transcribing. To see a list of supported languages, go check out [vosk-api](https://github.com/alphacep/vosk-api) documentation for more details.

The **text-to-speech** model uses the Kokoro engine which is a curated pipeline of pretrained voices fine-tuned for smoother, more expressive output. The [tts](https://github.com/kannachi323/dweller-speech/tree/main/tts) directory contains code for synthesizing speech from raw text, selecting voices, and managing audio playback. This allows Dweller to respond in a natural and flexible way. Please take a look at [kokoro](https://github.com/hexgrad/kokoro) and [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) for more examples and documentation.

## Purpose

The goal of `dweller-speech` is not to develop new speech-to-text (STT) or text-to-speech (TTS) models from scratch, but rather to **leverage powerful, existing open-source solutions** and make them easier to integrate into the Dweller ecosystem.

This repository provides a thin abstraction layer over tools like **Vosk** and **Kokoro**, offering:

- Wrapper classes for simplified model usage  
- Local server hosting for self-contained, offline operation  
- WebSocket endpoints for real-time communication with Dweller or other clients  

By providing these models with a modular interface, `dweller-speech` enables Dweller to speak and listen efficiently, while keeping the flexibility to swap or upgrade components as needed.

## Getting Started

### Dependencies



### Installation


### Usage


## Help

## Authors

[me :)](https://github.com/kannachi323)

## Version History


## License



## Acknowledgments


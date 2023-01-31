# wav2vec2-emotion-detection-ger
Detect emotions from spoken text. For inference, create a mono channel wav file.

Emotion classes are:
  - 0: 'anger'
  - 1: 'boredom'
  - 2: 'disgust'
  - 3: 'fear'
  - 4: 'happiness'
  - 5: 'sadness'
  - 6: 'neutral'

## Training
Download the emo-DB dataset from http://emodb.bilderbar.info/index-1024.html and unzip the wavs folder into the repositories main directory.
The necessary preprocessing is done in train.py.

## Inference
You can use my pretrained model from here https://huggingface.co/padmalcom/wav2vec2-large-emotion-detection-german
inference_local.py loads the model from a local folder (in case that you want to use the model offline) and inference_online.py downloads
the model from the huggingface hub.

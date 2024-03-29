from transformers.models.wav2vec2.modeling_wav2vec2 import (
	Wav2Vec2PreTrainedModel,
	Wav2Vec2Model
)
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss
import torch
from dataclasses import dataclass
from transformers.file_utils import ModelOutput
from typing import Dict, List, Optional, Union, Tuple, Any
from Wav2Vec2ClassificationHead import Wav2Vec2ClassificationHead

@dataclass
class SpeechClassifierOutput(ModelOutput):
	loss: Optional[torch.FloatTensor] = None
	logits: torch.FloatTensor = None
	hidden_states: Optional[Tuple[torch.FloatTensor]] = None
	attentions: Optional[Tuple[torch.FloatTensor]] = None
	
class Wav2Vec2ForSpeechClassification(Wav2Vec2PreTrainedModel):
	def __init__(self, config):
		super().__init__(config)
		self.num_labels = config.num_labels
		self.pooling_mode = config.pooling_mode
		self.config = config

		self.wav2vec2 = Wav2Vec2Model(config)
		self.classifier = Wav2Vec2ClassificationHead(config)

		self.init_weights()

	def freeze_feature_extractor(self):
		self.wav2vec2.feature_extractor._freeze_parameters()

	def forward(
			self,
			input_values,
			attention_mask=None,
			output_attentions=None,
			output_hidden_states=None,
			return_dict=None,
			labels=None,
	):
		return_dict = return_dict if return_dict is not None else self.config.use_return_dict
		outputs = self.wav2vec2(
			input_values,
			attention_mask=attention_mask,
			output_attentions=output_attentions,
			output_hidden_states=output_hidden_states,
			return_dict=return_dict,
		)
		hidden_states = outputs[0]
		hidden_states = torch.mean(hidden_states, dim=1)
		logits = self.classifier(hidden_states)

		loss_fct = CrossEntropyLoss()
		loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
				
		if not return_dict:
			output = (logits,) + outputs[2:]
			return ((loss,) + output) if loss is not None else output

		return SpeechClassifierOutput(
			loss=loss,
			logits=logits,
			hidden_states=outputs.hidden_states,
			attentions=outputs.attentions,
		)
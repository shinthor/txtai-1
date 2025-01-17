"""
Hugging Face pipeline wrapper module
"""

from transformers import pipeline

from .tensors import Tensors


class HFPipeline(Tensors):
    """
    Light wrapper around Hugging Face's pipeline component for selected tasks. Adds support for model
    quantization and minor interface changes.
    """

    def __init__(self, task, path=None, quantize=False, gpu=False, model=None):
        """
        Loads a new pipeline model.

        Args:
            task: pipeline task or category
            path: optional path to model, accepts Hugging Face model hub id or local path,
                  uses default model for task if not provided
            quantize: if model should be quantized, defaults to False
            gpu: True/False if GPU should be enabled, also supports a GPU device id
            model: optional existing pipeline model to wrap
        """

        if model:
            # Check if input model is a Pipeline or a HF pipeline
            self.pipeline = model.pipeline if isinstance(model, HFPipeline) else model
        else:
            # Get device id
            deviceid = self.deviceid(gpu)

            # Transformer pipeline task
            self.pipeline = pipeline(task, model=path, tokenizer=path, device=deviceid)

            # Model quantization. Compresses model to int8 precision, improves runtime performance. Only supported on CPU.
            if deviceid == -1 and quantize:
                # pylint: disable=E1101
                self.pipeline.model = self.quantize(self.pipeline.model)

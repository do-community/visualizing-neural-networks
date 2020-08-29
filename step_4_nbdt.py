"""Run evaluation on a single image, using an NBDT"""

from nbdt.model import SoftNBDT, HardNBDT
from pytorchcv.models.wrn_cifar import wrn28_10_cifar10
from torchvision import transforms
from nbdt.utils import DATASET_TO_CLASSES, load_image_from_path, maybe_install_wordnet
import sys

maybe_install_wordnet()


def get_model():
    """Load pretrained NBDT"""
    model = wrn28_10_cifar10()
    model = HardNBDT(
      pretrained=True,
      dataset='CIFAR10',
      arch='wrn28_10_cifar10',
      model=model)
    return model


def load_image():
    """Load + transform image"""
    assert len(sys.argv) > 1, "Need to pass image URL or image path as argument"
    im = load_image_from_path(sys.argv[1])
    transform = transforms.Compose([
      transforms.Resize(32),
      transforms.CenterCrop(32),
      transforms.ToTensor(),
      transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    x = transform(im)[None]
    return x


def print_explanation(outputs, decisions):
    """Print the prediction and decisions"""
    _, predicted = outputs.max(1)
    cls = DATASET_TO_CLASSES['CIFAR10'][predicted[0]]
    print('Prediction:', cls, '// Decisions:', ', '.join([
        '{} ({:.2f}%)'.format(info['name'], info['prob'] * 100) for info in decisions[0]
    ][1:]))  # [1:] to skip the root


def main():
    model = get_model()
    x = load_image()
    outputs, decisions = model.forward_with_decisions(x)  # use `model(x)` to obtain just logits
    print_explanation(outputs, decisions)


if __name__ == '__main__':
    main()
from typing import final

from dishka import Container, Provider, Scope, make_container, provide

from text_analyzer.application.commands.download_dataset import DownloadDatasetCommandHandler
from text_analyzer.application.commands.evaluate_model import EvaluateModelCommandHandler
from text_analyzer.application.commands.predict import PredictCommandHandler
from text_analyzer.application.commands.train_model import TrainModelCommandHandler
from text_analyzer.application.commands.visualize import VisualizeCommandHandler
from text_analyzer.application.ports.classifier import SentimentClassifier
from text_analyzer.application.ports.dataset_downloader import DatasetDownloader
from text_analyzer.application.ports.dataset_loader import DatasetLoader
from text_analyzer.application.ports.text_preprocessor import TextPreprocessor
from text_analyzer.application.ports.visualizer import TrainingVisualizer
from text_analyzer.infrastructure.file_dataset_loader import FileDatasetLoader
from text_analyzer.infrastructure.http_downloader import HttpDatasetDownloader
from text_analyzer.infrastructure.matplotlib_visualizer import MatplotlibVisualizer
from text_analyzer.infrastructure.pytorch_classifier import PytorchSentimentClassifier
from text_analyzer.infrastructure.simple_preprocessor import SimpleTextPreprocessor


@final
class InfrastructureProvider(Provider):
    scope = Scope.APP

    @provide
    def dataset_downloader(self) -> DatasetDownloader:
        return HttpDatasetDownloader()

    @provide
    def dataset_loader(self) -> DatasetLoader:
        return FileDatasetLoader()

    @provide
    def text_preprocessor(self) -> TextPreprocessor:
        return SimpleTextPreprocessor()

    @provide
    def classifier(self) -> SentimentClassifier:
        return PytorchSentimentClassifier()

    @provide
    def visualizer(self) -> TrainingVisualizer:
        return MatplotlibVisualizer()


@final
class ApplicationProvider(Provider):
    scope = Scope.APP

    @provide
    def download_handler(self, downloader: DatasetDownloader) -> DownloadDatasetCommandHandler:
        return DownloadDatasetCommandHandler(dataset_downloader=downloader)

    @provide
    def train_handler(
        self,
        loader: DatasetLoader,
        preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
    ) -> TrainModelCommandHandler:
        return TrainModelCommandHandler(
            dataset_loader=loader,
            text_preprocessor=preprocessor,
            classifier=classifier,
        )

    @provide
    def evaluate_handler(
        self,
        loader: DatasetLoader,
        preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
    ) -> EvaluateModelCommandHandler:
        return EvaluateModelCommandHandler(
            dataset_loader=loader,
            text_preprocessor=preprocessor,
            classifier=classifier,
        )

    @provide
    def predict_handler(
        self,
        preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
    ) -> PredictCommandHandler:
        return PredictCommandHandler(
            text_preprocessor=preprocessor,
            classifier=classifier,
        )

    @provide
    def visualize_handler(
        self,
        loader: DatasetLoader,
        preprocessor: TextPreprocessor,
        classifier: SentimentClassifier,
        visualizer: TrainingVisualizer,
    ) -> VisualizeCommandHandler:
        return VisualizeCommandHandler(
            dataset_loader=loader,
            text_preprocessor=preprocessor,
            classifier=classifier,
            visualizer=visualizer,
        )


def create_container() -> Container:
    return make_container(InfrastructureProvider(), ApplicationProvider())

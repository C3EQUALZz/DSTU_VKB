import click
from dishka import Container, make_container
from dishka.integrations.click import setup_dishka

from vulnfinder.setup.bootstrap import setup_logging, setup_configs, setup_cli_routes
from vulnfinder.setup.configs.app_config import ApplicationConfig
from vulnfinder.setup.configs.knowledge_base_config import KnowledgeBaseConfig
from vulnfinder.setup.configs.open_router_config import OpenRouterConfig
from vulnfinder.setup.configs.vector_store_config import ChromaDBVectorStoreConfig
from vulnfinder.setup.ioc import setup_providers


@click.group()
@click.pass_context
def main(context: click.Context) -> None:
    config: ApplicationConfig = setup_configs()

    setup_logging(config.logging)

    dishka_context = {
        KnowledgeBaseConfig: config.knowledge_base,
        OpenRouterConfig: config.open_router_config,
        ChromaDBVectorStoreConfig: config.chromadb_vector_store,
    }

    container: Container = make_container(
        *setup_providers(),
        context=dishka_context,
    )

    setup_dishka(container, context=context, auto_inject=True)

setup_cli_routes(main)

if __name__ == "__main__":
    main()

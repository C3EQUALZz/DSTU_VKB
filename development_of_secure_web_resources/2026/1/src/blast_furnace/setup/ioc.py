from dishka import Provider, Scope, provide

from blast_furnace.application.get_blast_reference import GetBlastReference


class ApplicationProvider(Provider):
    reference_query = provide(GetBlastReference, scope=Scope.REQUEST)

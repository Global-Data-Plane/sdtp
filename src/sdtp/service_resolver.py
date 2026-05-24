class ServiceResolver:
    '''
    Resolves logical service names to actual URLs depending on deployment environment.
    '''

    def __init__(self):
        self.resolvers = {
            "docker-compose": self._docker_compose_url,
            "kubernetes": self._kubernetes_url,
            "cloud-run": self._cloud_run_url,
        }

    def resolve(self, service_name: str, deployment: str = "docker-compose") -> str:
        resolver = self.resolvers.get(deployment)
        if not resolver:
            raise InvalidDataException(f"Unknown deployment type: {deployment}")
        return resolver(service_name)

    def _docker_compose_url(self, service_name: str) -> str:
        return f"http://{service_name}:8080"

    def _kubernetes_url(self, service_name: str) -> str:
        # Adjust namespace as needed
        return f"http://{service_name}.default.svc.cluster.local:8080"

    def _cloud_run_url(self, service_name: str) -> str:
        # Cloud Run sidecar pattern - usually localhost or internal DNS
        return f"http://{service_name}:8080"
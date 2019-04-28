class LocalServiceNotFoundError(AttributeError):
    def __init__(self, local_service_directory):
        local_services_with_config = ", ".join(list(local_service_directory.keys()))
        super().__init__(
            f"Service not found. Local services with config "
            f"are: {local_services_with_config}"
        )

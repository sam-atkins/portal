class ServiceNotFoundError(AttributeError):
    def __init__(self, service_directory):
        local_services_with_config = ", ".join(list(service_directory.keys()))
        super().__init__(
            f"Service not found. Local services with config "
            f"are: {local_services_with_config}"
        )


class ServiceFunctionNotFoundError(AttributeError):
    def __init__(self, lambda_config):
        functions_with_config = ", ".join(list(lambda_config.keys()))
        super().__init__(
            f"Function not found. Available functions: {functions_with_config}"
        )

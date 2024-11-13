import sys

file_path = sys.argv[1]
version = sys.argv[2]
branch = sys.argv[3]
sas_token = sys.argv[4] if len(sys.argv) ==5 else ''

with open(file_path, "r") as file:
    content = file.read()

    content = content.replace("<bg-search-version-here>", version)
    content = content.replace("IS_SNP: <ENABLE_SP_ASSETS>", "IS_SNP: false")
    content = content.replace("SAS_TOKEN: <TOKEN>", "SAS_TOKEN: {}".format(sas_token)) 
    if branch == "refs/heads/main":
        content = content.replace("<env-tag>", "latest")
        content = content.replace(
            "<image_src_w_prefix>", f"/spdemo/data_schema/alcyone_repository/")

        content = content.replace("<openTelemetry_logging>", "")
        content = content.replace(
            "OTEL_TRACING: <enable_tracing>", "OTEL_TRACING: false")

    elif branch == 'refs/heads/stage':
        content = content.replace("<env-tag>", "stage")
        content = content.replace(
            "<image_src_w_prefix>", f"/spdemo/data_schema/alcyone_repository/")

        content = content.replace("<openTelemetry_logging>",
                                  '''- name: jaeger\r\n      image: /spdemo/data_schema/alcyone_repository/jaegertracing-all-in-one:1.58\r\n      env:\r\n        COLLECTOR_ZIPKIN_HOST_PORT: 9411\r\n        QUERY_BASE_PATH: /jaeger''')
        content = content.replace(
            "OTEL_TRACING: <enable_tracing>", "OTEL_TRACING: true")
        
    elif branch == 'refs/heads/pre-stage':
        content = content.replace("<env-tag>", "stage")
        content = content.replace(
            "<image_src_w_prefix>", f"/spdemo/data_schema/alcyone_repository/")

        content = content.replace("<openTelemetry_logging>",
                                  '''- name: jaeger\r\n      image: /spdemo/data_schema/alcyone_repository/jaegertracing-all-in-one:1.58\r\n      env:\r\n        COLLECTOR_ZIPKIN_HOST_PORT: 9411\r\n        QUERY_BASE_PATH: /jaeger''')
        content = content.replace(
            "OTEL_TRACING: <enable_tracing>", "OTEL_TRACING: true")

    elif branch == 'refs/heads/SP':
        content = content.replace("<env-tag>", "snp")
        content = content.replace("IS_SNP: false", "IS_SNP: true")
        content = content.replace(
            "<image_src_w_prefix>", f"/spdemo/data_schema/alcyone_repository/")
        content = content.replace("<openTelemetry_logging>","")
        content = content.replace(
            "OTEL_TRACING: <enable_tracing>", "OTEL_TRACING: true")


    else:
        content = content.replace("<env-tag>", "latest")
        content = content.replace(
            "<image_src_w_prefix>", f"/bg_dev/data_schema_stage/bg_dev/{branch.split('/')[-1]}_")
        content = content.replace("<openTelemetry_logging>",
                                  '''- name: jaeger\r\n      image: /spdemo/data_schema/alcyone_repository/jaegertracing-all-in-one:1.58\r\n      env:\r\n        COLLECTOR_ZIPKIN_HOST_PORT: 9411\r\n        QUERY_BASE_PATH: /jaeger''')
        content = content.replace(
            "OTEL_TRACING: <enable_tracing>", "OTEL_TRACING: true")

with open(file_path, "w") as file:
    file.write(content)

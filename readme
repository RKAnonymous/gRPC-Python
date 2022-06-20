Simple CRUD gRPC server and client - Python implementation


            Setup environment for project and activate

1. python3 -m venv project_env
2. source project_env/bin/activate


            Installing required packages

3. pip install -r requirements.txt


            Making necessary directories as environment variables

4. export PYTHONPATH="$PYTHONPATH:/path/to/gprc_project"
5. export MONGODB_URI=...


            Generate server and client side protocol code

6. python3 -m grpc_tools.protoc --proto_path=../protos/ --python_out=. --grpc_python_out=. blog.proto


            Running the server service

7. python3 blog/server.py

            Running the client service

8. python3 blog/client.py
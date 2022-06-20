Simple CRUD gRPC server and client - Python implementation


1. Setup environment for project and activate

           python3 -m venv project_env
           source project_env/bin/activate


2. Installing required packages

           pip install -r requirements.txt


3. Making necessary directories as environment variables

           export PYTHONPATH="$PYTHONPATH:/path/to/gprc_project"
           export MONGODB_URI=mongodb://username:password@host:port


4. Generate server and client side protocol code

           python3 -m grpc_tools.protoc --proto_path=../protos/ --python_out=. --grpc_python_out=. blog.proto


5. Running the server service

           python3 blog/server.py

6. Running the client service

           python3 blog/client.py
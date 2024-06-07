# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

FROM public.ecr.aws/lambda/python:3.11

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN pip install -r requirements.txt
# Switch to the non-privileged user to run the application.
# USER appuser

# Copy the source code into the container.
# COPY . .

COPY lambda/lambda_function.py ${LAMBDA_TASK_ROOT}
# COPY cdk.out cdk.out

# Expose the port that the application listens on.
# EXPOSE 9000

# Ensure handler has executable permissions
RUN chmod +x ${LAMBDA_TASK_ROOT}/lambda_function.py

# Run the application.
CMD ["lambda_function.lambda_handler"]
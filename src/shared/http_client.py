"""
HTTP Client implementation using the requests library.

This module provides a comprehensive HTTP client that implements all common HTTP verbs
with proper error handling, logging, and response validation.
"""

import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPClient:
    """
    A comprehensive HTTP client implementation using the requests library.

    This client provides methods for all common HTTP verbs and includes features like:
    - Automatic retries with exponential backoff
    - Request/response logging
    - Error handling and validation
    - Session management for connection pooling
    - Support for custom headers, timeouts, and authentication
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: tuple = (500, 502, 504),
        headers: dict = {},
        verify_ssl: bool = True,
        logger: logging.Logger | None = None,
    ):
        """
        Initialize the HTTP client.

        Args:
            base_url: Base URL for all requests (optional)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            backoff_factor: Backoff factor for retry delays
            status_forcelist: HTTP status codes that should trigger a retry
            headers: Default headers to include with all requests
            verify_ssl: Whether to verify SSL certificates
            logger: Custom logger instance (optional)
        """
        self._default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self.base_url = base_url
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

        # Create session for connection pooling
        self.session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=[
                "HEAD",
                "GET",
                "PUT",
                "DELETE",
                "OPTIONS",
                "TRACE",
                "POST",
                "PATCH",
            ],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        headers.update(self._default_headers)
        self.session.headers.update(headers)

        # Set SSL verification
        self.session.verify = verify_ssl

    def _build_url(self, url: str) -> str:
        """Build the full URL by joining with base_url if provided."""
        if self.base_url:
            return f"{self.base_url}/{url.lstrip('/')}"
        return url

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log the outgoing request."""
        self.logger.info(f"Making {method.upper()} request to {url}")
        if kwargs.get("params"):
            self.logger.debug(f"Query params: {kwargs['params']}")
        if kwargs.get("json"):
            self.logger.debug(f"Request body (JSON): {kwargs['json']}")
        if kwargs.get("data"):
            self.logger.debug(f"Request body (data): {kwargs['data']}")

    def _log_response(self, response: requests.Response) -> None:
        """Log the response details."""
        self.logger.info(f"Response: {response.status_code} {response.reason}")
        self.logger.debug(f"Response headers: {dict(response.headers)}")
        if response.text:
            self.logger.debug(f"Response body: {response.text[:500]}...")

    def _make_request(
        self, method: str, url: str, raise_for_status: bool = True, **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request with the given method.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: URL to make the request to
            raise_for_status: Whether to raise an exception for HTTP error status codes
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object

        Raises:
            requests.RequestException: If the request fails
        """
        full_url = self._build_url(url)

        # Set default timeout if not provided
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        self._log_request(method, full_url, **kwargs)

        try:
            response = self.session.request(method, full_url, **kwargs)
            self._log_response(response)

            if raise_for_status:
                response.raise_for_status()

            return response

        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise

    def get(
        self,
        url: str,
        params: dict | None = None,
        headers: dict = {},
        **kwargs,
    ) -> requests.Response:
        """
        Make a GET request.

        Args:
            url: URL to make the request to
            params: Query parameters
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object
        """
        return self._make_request("GET", url, params=params, headers=headers, **kwargs)

    def post(
        self,
        url: str,
        data: dict | str | bytes | None = None,
        json: dict | None = None,
        headers: dict = {},
        **kwargs,
    ) -> requests.Response:
        """
        Make a POST request.

        Args:
            url: URL to make the request to
            data: Request body data
            json: JSON data to send
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object
        """
        return self._make_request(
            "POST", url, data=data, json=json, headers=headers, **kwargs
        )

    def put(
        self,
        url: str,
        data: dict | str | bytes | None = None,
        json: dict | None = None,
        headers: dict = {},
        **kwargs,
    ) -> requests.Response:
        """
        Make a PUT request.

        Args:
            url: URL to make the request to
            data: Request body data
            json: JSON data to send
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object
        """
        return self._make_request(
            "PUT", url, data=data, json=json, headers=headers, **kwargs
        )

    def patch(
        self,
        url: str,
        data: dict | str | bytes | None = None,
        json: dict | None = None,
        headers: dict = {},
        **kwargs,
    ) -> requests.Response:
        """
        Make a PATCH request.

        Args:
            url: URL to make the request to
            data: Request body data
            json: JSON data to send
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object
        """
        return self._make_request(
            "PATCH", url, data=data, json=json, headers=headers, **kwargs
        )

    def delete(self, url: str, headers: dict = {}, **kwargs) -> requests.Response:
        """
        Make a DELETE request.

        Args:
            url: URL to make the request to
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object
        """
        return self._make_request("DELETE", url, headers=headers, **kwargs)

    def head(self, url: str, headers: dict = {}, **kwargs) -> requests.Response:
        """
        Make a HEAD request.

        Args:
            url: URL to make the request to
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object
        """
        return self._make_request("HEAD", url, headers=headers, **kwargs)

    def options(self, url: str, headers: dict = {}, **kwargs) -> requests.Response:
        """
        Make an OPTIONS request.

        Args:
            url: URL to make the request to
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The response object
        """
        return self._make_request("OPTIONS", url, headers=headers, **kwargs)

    def close(self) -> None:
        """Close the session and free up resources."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience function to create a client instance
def create_client(
    base_url: str | None = None,
    timeout: int = 30,
    max_retries: int = 3,
    headers: dict = {},
    **kwargs,
) -> HTTPClient:
    """
    Create a new HTTPClient instance with the given configuration.

    Args:
        base_url: Base URL for all requests
        timeout: Request timeout in seconds
        max_retries: Maximum number of retries
        headers: Default headers
        **kwargs: Additional configuration options

    Returns:
        HTTPClient: A configured HTTP client instance
    """
    return HTTPClient(
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
        headers=headers,
        **kwargs,
    )

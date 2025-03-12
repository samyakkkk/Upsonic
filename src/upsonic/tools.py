"""
Upsonic Tools Module
This module contains the tool implementations that can be used with Upsonic.
"""
from typing import Any, List, Dict, Optional, Type, Union, Callable
import os
import json
import requests
import logging
import pathlib
from datetime import datetime
import time
import re
from .client.printing import missing_dependencies, missing_api_key

class Search:
    pass



class ComputerUse:
    pass

class BrowserUse:
    pass



class Wikipedia:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for Wikipedia and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "wikipedia": False
        }
        
        # Check each dependency
        try:
            import wikipedia
            dependencies["wikipedia"] = True
        except ImportError:
            pass
        
        return dependencies
        
    @staticmethod
    def __control__() -> bool:
        # Check the import wikipedia
        try:
            import wikipedia
            return True
        except ImportError:
            # Use the missing_dependencies function to display the error
            missing_dependencies("Wikipedia", ["wikipedia"])
            raise ImportError("Missing dependency: wikipedia. Please install it with: pip install wikipedia")
        
    def search(query: str) -> str:
        import wikipedia
        return wikipedia.search(query)
    
    def summary(query: str) -> str:
        import wikipedia
        return wikipedia.summary(query)


class DuckDuckGo:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for DuckDuckGo and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "duckduckgo_search": False
        }
        
        # Check each dependency
        try:
            import duckduckgo_search
            dependencies["duckduckgo_search"] = True
        except ImportError:
            pass
        
        return dependencies
        
    @staticmethod
    def __control__() -> bool:
        # Check the import duckduckgo_search
        try:
            import duckduckgo_search
            return True
        except ImportError:
            # Use the missing_dependencies function to display the error
            missing_dependencies("DuckDuckGo", ["duckduckgo_search"])
            raise ImportError("Missing dependency: duckduckgo_search. Please install it with: pip install duckduckgo-search")
    
    def search(query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search DuckDuckGo for the given query and return text results.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return (default: 10)
            
        Returns:
            List of dictionaries containing search results with keys: title, href, body
        """
        from duckduckgo_search import DDGS
        
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))
        return results
    

class SerperDev:
    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Try to load the SERPER_API_KEY from a .env file using python-dotenv.
        
        Returns:
            The API key if found in .env file, None otherwise
        """
        try:
            # Try to import dotenv
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError("python-dotenv is not installed. Please install it with 'pip install python-dotenv'")
        
        # Check for .env file in current directory and parent directories
        current_dir = pathlib.Path.cwd()
        
        # Look in current directory and up to 3 parent directories
        for _ in range(4):
            env_path = current_dir / '.env'
            if env_path.exists():
                # Load the .env file
                load_dotenv(dotenv_path=env_path)
                
                # Check if SERPER_API_KEY is now in environment
                if "SERPER_API_KEY" in os.environ:
                    return os.environ["SERPER_API_KEY"]
            
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root directory
                break
            current_dir = parent_dir
        
        return None
    
    def __control__(self) -> bool:
        # Check if requests is installed
        try:
            import requests
        except ImportError:
            raise ImportError("requests is not installed. Please install it with 'pip install requests'")
        
        # Check if SERPER_API_KEY is set in environment variables
        if "SERPER_API_KEY" not in os.environ:
            try:
                # Try to load API key from .env file
                api_key = SerperDev._load_api_key_from_env_file()
                if api_key is None:
                    # API key not found in .env file
                    missing_api_key("SerperDev", "SERPER_API_KEY")
                    raise EnvironmentError("SERPER_API_KEY environment variable is not set and could not be found in .env file")
            except ImportError:
                # If dotenv is not installed, we can't load from .env file
                missing_api_key("SerperDev", "SERPER_API_KEY", dotenv_support=False)
                raise EnvironmentError("SERPER_API_KEY environment variable is not set and python-dotenv is not installed")
        
        return True
    
    def __init__(self, base_url: str = "https://google.serper.dev", search_type: str = "search", n_results: int = 10, country: str = "us", 
                 location: str = None, locale: str = "en", api_key: Optional[str] = None):
        """
        Initialize the SerperDev search tool.
        
        Args:
            base_url: Base URL for the Serper API (default: "https://google.serper.dev")
            search_type: Type of search to perform (default: "search")
            n_results: Number of results to return (default: 10)
            country: Country code for search (default: "us")
            location: Location for search (default: None)
            locale: Locale for search (default: "en")
            api_key: Serper API key (optional, will try to load from environment if not provided)
        """
        self.base_url = base_url
        self.search_type = search_type
        self.n_results = n_results
        self.country = country
        self.location = location
        self.locale = locale
        
        # Set API key
        self.api_key = api_key
        
        # If API key not provided, try to load from environment or .env file
        if self.api_key is None:
            # First check environment variables
            if "SERPER_API_KEY" in os.environ:
                self.api_key = os.environ["SERPER_API_KEY"]
            else:
                # Try to load from .env file
                try:
                    api_key = self._load_api_key_from_env_file()
                    if api_key:
                        self.api_key = api_key
                    else:
                        # Print missing API key message
                        missing_api_key("SerperDev", "SERPER_API_KEY")
                        raise EnvironmentError("SERPER_API_KEY environment variable is not set and could not be found in .env file")
                except ImportError:
                    # If dotenv is not installed and no API key in environment
                    if "SERPER_API_KEY" not in os.environ:
                        # Print missing API key message without dotenv support
                        missing_api_key("SerperDev", "SERPER_API_KEY", dotenv_support=False)
                        raise EnvironmentError("SERPER_API_KEY environment variable is not set and python-dotenv is not installed")
                    self.api_key = os.environ["SERPER_API_KEY"]

    def _get_search_url(self) -> str:
        """Get the appropriate endpoint URL based on search type."""
        search_type = self.search_type.lower()
        allowed_search_types = ["search", "news"]
        if search_type not in allowed_search_types:
            raise ValueError(
                f"Invalid search type: {search_type}. Must be one of: {', '.join(allowed_search_types)}"
            )
        return f"{self.base_url}/{search_type}"

    def _process_knowledge_graph(self, kg: dict) -> dict:
        """Process knowledge graph data from search results."""
        return {
            "title": kg.get("title", ""),
            "type": kg.get("type", ""),
            "website": kg.get("website", ""),
            "imageUrl": kg.get("imageUrl", ""),
            "description": kg.get("description", ""),
            "descriptionSource": kg.get("descriptionSource", ""),
            "descriptionLink": kg.get("descriptionLink", ""),
            "attributes": kg.get("attributes", {}),
        }

    def _process_organic_results(self, organic_results: list) -> list:
        """Process organic search results."""
        processed_results = []
        for result in organic_results[:self.n_results]:
            try:
                result_data = {
                    "title": result["title"],
                    "link": result["link"],
                    "snippet": result.get("snippet", ""),
                    "position": result.get("position"),
                }

                if "sitelinks" in result:
                    result_data["sitelinks"] = [
                        {
                            "title": sitelink.get("title", ""),
                            "link": sitelink.get("link", ""),
                        }
                        for sitelink in result["sitelinks"]
                    ]

                processed_results.append(result_data)
            except KeyError:
                continue
        return processed_results

    def _process_people_also_ask(self, paa_results: list) -> list:
        """Process 'People Also Ask' results."""
        processed_results = []
        for result in paa_results[:self.n_results]:
            try:
                result_data = {
                    "question": result["question"],
                    "snippet": result.get("snippet", ""),
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                }
                processed_results.append(result_data)
            except KeyError:
                continue
        return processed_results

    def _process_related_searches(self, related_results: list) -> list:
        """Process related search results."""
        processed_results = []
        for result in related_results[:self.n_results]:
            try:
                processed_results.append({"query": result["query"]})
            except KeyError:
                continue
        return processed_results

    def _process_news_results(self, news_results: list) -> list:
        """Process news search results."""
        processed_results = []
        for result in news_results[:self.n_results]:
            try:
                result_data = {
                    "title": result["title"],
                    "link": result["link"],
                    "snippet": result.get("snippet", ""),
                    "date": result.get("date", ""),
                    "source": result.get("source", ""),
                    "imageUrl": result.get("imageUrl", ""),
                }
                processed_results.append(result_data)
            except KeyError:
                continue
        return processed_results

    def _process_search_results(self, results: dict) -> dict:
        """Process search results based on search type."""
        formatted_results = {}

        if self.search_type == "search":
            if "knowledgeGraph" in results:
                formatted_results["knowledgeGraph"] = self._process_knowledge_graph(
                    results["knowledgeGraph"]
                )

            if "organic" in results:
                formatted_results["organic"] = self._process_organic_results(
                    results["organic"]
                )

            if "peopleAlsoAsk" in results:
                formatted_results["peopleAlsoAsk"] = self._process_people_also_ask(
                    results["peopleAlsoAsk"]
                )

            if "relatedSearches" in results:
                formatted_results["relatedSearches"] = self._process_related_searches(
                    results["relatedSearches"]
                )

        elif self.search_type == "news":
            if "news" in results:
                formatted_results["news"] = self._process_news_results(results["news"])

        return formatted_results

    def search(self, query: str) -> Dict[str, Any]:
        print("*************I am here")
        print(self.api_key)

        print(self.base_url)
        print(query)
        """
        Search the web using Serper API.
        
        Args:
            query: The search query
            
        Returns:
            Dictionary containing processed search results
        """
        search_url = self._get_search_url()
        payload = json.dumps({"q": query, "num": self.n_results})
        
        if self.country:
            payload = json.dumps(json.loads(payload) | {"gl": self.country})
        
        if self.location:
            payload = json.dumps(json.loads(payload) | {"location": self.location})
            
        if self.locale:
            payload = json.dumps(json.loads(payload) | {"hl": self.locale})
            
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                search_url, headers=headers, json=json.loads(payload), timeout=10
            )
            response.raise_for_status()
            results = response.json()
            
            if not results:
                raise ValueError("Empty response from Serper API")
                
            formatted_results = {
                "searchParameters": {
                    "q": query,
                    "type": self.search_type,
                    **results.get("searchParameters", {}),
                }
            }

            formatted_results.update(self._process_search_results(results))
            formatted_results["credits"] = results.get("credits", 1)
            
            return formatted_results
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error making request to Serper API: {e}"
            raise RuntimeError(error_msg)
        except json.JSONDecodeError as e:
            error_msg = f"Error decoding JSON response: {e}"
            raise RuntimeError(error_msg)


class OlostepScrapeWebsiteTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for OlostepScrapeWebsiteTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "requests": False,
            "python-dotenv": False
        }
        
        # Check each dependency
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencies["python-dotenv"] = True
        except ImportError:
            pass
        
        return dependencies
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and API key is available.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
            EnvironmentError: If API key is not available
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("OlostepScrapeWebsiteTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        # Check if OLOSTEP_API_KEY is set in environment variables
        if "OLOSTEP_API_KEY" not in os.environ:
            try:
                # Try to load API key from .env file
                api_key = OlostepScrapeWebsiteTool._load_api_key_from_env_file()
                if api_key is None:
                    # API key not found in .env file
                    missing_api_key("OlostepScrapeWebsiteTool", "OLOSTEP_API_KEY")
                    raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and could not be found in .env file")
            except ImportError:
                # If dotenv is not installed, we can't load from .env file
                missing_api_key("OlostepScrapeWebsiteTool", "OLOSTEP_API_KEY", dotenv_support=False)
                raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and python-dotenv is not installed")
        
        return True
    
    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Try to load the OLOSTEP_API_KEY from a .env file using python-dotenv.
        
        Returns:
            The API key if found in .env file, None otherwise
        """
        try:
            # Try to import dotenv
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError("python-dotenv is not installed. Please install it with 'pip install python-dotenv'")
        
        # Check for .env file in current directory and parent directories
        current_dir = pathlib.Path.cwd()
        
        # Look in current directory and up to 3 parent directories
        for _ in range(4):
            env_path = current_dir / '.env'
            if env_path.exists():
                # Load the .env file
                load_dotenv(dotenv_path=env_path)
                
                # Check if OLOSTEP_API_KEY is now in environment
                if "OLOSTEP_API_KEY" in os.environ:
                    return os.environ["OLOSTEP_API_KEY"]
            
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root directory
                break
            current_dir = parent_dir
        
        return None
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.olostep.com/v1"):
        """
        Initialize the OlostepScrapeWebsiteTool.
        
        Args:
            api_key: Olostep API key (optional, will try to load from environment if not provided)
            base_url: Base URL for the Olostep API (default: "https://api.olostep.com/v1")
        """
        # Set API key
        self.api_key = api_key
        self.base_url = base_url
        
        # If API key not provided, try to load from environment or .env file
        if self.api_key is None:
            # First check environment variables
            if "OLOSTEP_API_KEY" in os.environ:
                self.api_key = os.environ["OLOSTEP_API_KEY"]
            else:
                # Try to load from .env file
                try:
                    api_key = self._load_api_key_from_env_file()
                    if api_key:
                        self.api_key = api_key
                    else:
                        # Print missing API key message
                        missing_api_key("OlostepScrapeWebsiteTool", "OLOSTEP_API_KEY")
                        raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and could not be found in .env file")
                except ImportError:
                    # If dotenv is not installed and no API key in environment
                    if "OLOSTEP_API_KEY" not in os.environ:
                        # Print missing API key message without dotenv support
                        missing_api_key("OlostepScrapeWebsiteTool", "OLOSTEP_API_KEY", dotenv_support=False)
                        raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and python-dotenv is not installed")
                    self.api_key = os.environ["OLOSTEP_API_KEY"]
        
        # Check if requests is installed
        try:
            import requests
        except ImportError:
            missing_dependencies("OlostepScrapeWebsiteTool", ["requests"])
            raise ImportError("requests is not installed. Please install it with 'pip install requests'")
    
    def scrape_website(self, url: str, wait_before_scraping: int = 0, country: str = None) -> Dict[str, Any]:
        """
        Scrape a website using Olostep API.
        
        Args:
            url: Website URL to scrape
            wait_before_scraping: Time to wait in milliseconds before starting the scrape (default: 0)
            country: Residential country to load the request from (e.g., "US", "CA", "GB")
            
        Returns:
            String containing markdown_content from the scraped website
        """
        import requests
        
        # Prepare request data
        data = {
            "url_to_scrape": url,
            "wait_before_scraping": wait_before_scraping,
            "formats": ["markdown"],
        }
        
        # Add optional parameters if provided
        if country:
            data["country"] = country
        
        # Set headers for the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Make the API request
        response = requests.post(f"{self.base_url}/scrapes", headers=headers, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            # Extract the relevant information from the response
            return response_data.get("result", {}).get("markdown_content", "")
        else:
            error_message = f"Error scraping website: {response.status_code} - {response.text}"
            raise Exception(error_message)


class OlostepWebSearchTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for OlostepWebSearchTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "requests": False,
            "python-dotenv": False
        }
        
        # Check each dependency
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencies["python-dotenv"] = True
        except ImportError:
            pass
        
        return dependencies
    
    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Try to load the OLOSTEP_API_KEY from a .env file using python-dotenv.
        
        Returns:
            The API key if found in .env file, None otherwise
        """
        try:
            # Try to import dotenv
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError("python-dotenv is not installed. Please install it with 'pip install python-dotenv'")
        
        # Check for .env file in current directory and parent directories
        current_dir = pathlib.Path.cwd()
        
        # Look in current directory and up to 3 parent directories
        for _ in range(4):
            env_path = current_dir / '.env'
            if env_path.exists():
                # Load the .env file
                load_dotenv(dotenv_path=env_path)
                
                # Check if OLOSTEP_API_KEY is now in environment
                if "OLOSTEP_API_KEY" in os.environ:
                    return os.environ["OLOSTEP_API_KEY"]
            
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root directory
                break
            current_dir = parent_dir
        
        return None
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and API key is available.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
            EnvironmentError: If API key is not available
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("OlostepWebSearchTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        # Check if OLOSTEP_API_KEY is set in environment variables
        if "OLOSTEP_API_KEY" not in os.environ:
            try:
                # Try to load API key from .env file
                api_key = OlostepWebSearchTool._load_api_key_from_env_file()
                if api_key is None:
                    # Print missing API key message
                    missing_api_key("OlostepWebSearchTool", "OLOSTEP_API_KEY")
                    raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and could not be found in .env file")
            except ImportError:
                # If dotenv is not installed, we can't load from .env file
                # Print missing API key message without dotenv support
                missing_api_key("OlostepWebSearchTool", "OLOSTEP_API_KEY", dotenv_support=False)
                raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and python-dotenv is not installed")
        
        return True
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.olostep.com/v1"):
        """
        Initialize the OlostepWebSearchTool tool.
        
        Args:
            api_key: Olostep API key (optional, will try to load from environment if not provided)
            base_url: Base URL for the Olostep API (default: "https://api.olostep.com/v1")
        """
        # Set API key
        self.api_key = api_key
        self.base_url = base_url
        
        # If API key not provided, try to load from environment or .env file
        if self.api_key is None:
            # First check environment variables
            if "OLOSTEP_API_KEY" in os.environ:
                self.api_key = os.environ["OLOSTEP_API_KEY"]
            else:
                # Try to load from .env file
                try:
                    api_key = self._load_api_key_from_env_file()
                    if api_key:
                        self.api_key = api_key
                    else:
                        # Print missing API key message
                        missing_api_key("OlostepWebSearchTool", "OLOSTEP_API_KEY")
                        raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and could not be found in .env file")
                except ImportError:
                    # If dotenv is not installed and no API key in environment
                    if "OLOSTEP_API_KEY" not in os.environ:
                        # Print missing API key message without dotenv support
                        missing_api_key("OlostepWebSearchTool", "OLOSTEP_API_KEY", dotenv_support=False)
                        raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and python-dotenv is not installed")
                    self.api_key = os.environ["OLOSTEP_API_KEY"]
        
        # Check if requests is installed
        try:
            import requests
        except ImportError:
            missing_dependencies("OlostepWebSearchTool", ["requests"])
            raise ImportError("requests is not installed. Please install it with 'pip install requests'")
    
    def search(self, query: str, country: str = "us", language: str = "en") -> Dict[str, Any]:
        """
        Search the web using Olostep SERP API.
        
        Args:
            query: The search query
            country: Country code for search results (default: 'us')
            language: Language code for search results (default: 'en')
            
        Returns:
            Search results from Olostep SERP API
        """
        import requests
        
        # Construct the Google search URL
        search_url = f"https://www.google.com/search?q={query}&gl={country}&hl={language}"
        
        # Prepare the API request
        endpoint = f"{self.base_url}/scrapes"
        
        payload = {
            "formats": ["parser_extract"],
            "parser_extract": {"parser_id": "@olostep/google-search"},
            "url_to_scrape": search_url
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Make the API request
            response = requests.post(endpoint, json=payload, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                
                # Extract the JSON content from the result
                if "result" in result and "json_content" in result["result"]:
                    import json
                    return json.loads(result["result"]["json_content"])
                
                return result
            else:
                # Handle API errors
                error_message = f"Olostep API request failed with status code {response.status_code}: {response.text}"
                print(error_message)
                return {"error": error_message}
                
        except Exception as e:
            # Handle any exceptions
            error_message = f"Error during Olostep API request: {str(e)}"
            print(error_message)
            return {"error": error_message}


class OlostepCrawlWebsiteTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for OlostepCrawlWebsiteTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "requests": False,
            "python-dotenv": False
        }
        
        # Check each dependency
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencies["python-dotenv"] = True
        except ImportError:
            pass
        
        return dependencies
    
    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Try to load the OLOSTEP_API_KEY from a .env file using python-dotenv.
        
        Returns:
            The API key if found in .env file, None otherwise
        """
        try:
            # Try to import dotenv
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError("python-dotenv is not installed. Please install it with 'pip install python-dotenv'")
        
        # Check for .env file in current directory and parent directories
        current_dir = pathlib.Path.cwd()
        
        # Look in current directory and up to 3 parent directories
        for _ in range(4):
            env_path = current_dir / '.env'
            if env_path.exists():
                # Load the .env file
                load_dotenv(dotenv_path=env_path)
                
                # Check if OLOSTEP_API_KEY is now in environment
                if "OLOSTEP_API_KEY" in os.environ:
                    return os.environ["OLOSTEP_API_KEY"]
            
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root directory
                break
            current_dir = parent_dir
        
        return None
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and API key is available.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
            EnvironmentError: If API key is not available
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("OlostepCrawlWebsiteTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        # Check if OLOSTEP_API_KEY is set in environment variables
        if "OLOSTEP_API_KEY" not in os.environ:
            try:
                # Try to load API key from .env file
                api_key = OlostepCrawlWebsiteTool._load_api_key_from_env_file()
                if api_key is None:
                    # Print missing API key message
                    missing_api_key("OlostepCrawlWebsiteTool", "OLOSTEP_API_KEY")
                    raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and could not be found in .env file")
            except ImportError:
                # If dotenv is not installed, we can't load from .env file
                # Print missing API key message without dotenv support
                missing_api_key("OlostepCrawlWebsiteTool", "OLOSTEP_API_KEY", dotenv_support=False)
                raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and python-dotenv is not installed")
        
        return True
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.olostep.com/v1"):
        """
        Initialize the OlostepCrawlWebsiteTool.
        
        Args:
            api_key: Olostep API key (optional, will try to load from environment if not provided)
            base_url: Base URL for the Olostep API (default: "https://api.olostep.com/v1")
        """
        # Set API key
        self.api_key = api_key
        self.base_url = base_url
        
        # If API key not provided, try to load from environment or .env file
        if self.api_key is None:
            # First check environment variables
            if "OLOSTEP_API_KEY" in os.environ:
                self.api_key = os.environ["OLOSTEP_API_KEY"]
            else:
                # Try to load from .env file
                try:
                    api_key = self._load_api_key_from_env_file()
                    if api_key:
                        self.api_key = api_key
                    else:
                        # Print missing API key message
                        missing_api_key("OlostepCrawlWebsiteTool", "OLOSTEP_API_KEY")
                        raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and could not be found in .env file")
                except ImportError:
                    # If dotenv is not installed and no API key in environment
                    if "OLOSTEP_API_KEY" not in os.environ:
                        # Print missing API key message without dotenv support
                        missing_api_key("OlostepCrawlWebsiteTool", "OLOSTEP_API_KEY", dotenv_support=False)
                        raise EnvironmentError("OLOSTEP_API_KEY environment variable is not set and python-dotenv is not installed")
                    self.api_key = os.environ["OLOSTEP_API_KEY"]
        
        # Check if requests is installed
        try:
            import requests
        except ImportError:
            missing_dependencies("OlostepCrawlWebsiteTool", ["requests"])
            raise ImportError("requests is not installed. Please install it with 'pip install requests'")
    
    def crawl_website(self, start_url: str, max_pages: int = 50) -> str:
        """
        Crawl a website using Olostep API and return all crawled content as a single formatted string.
        
        Args:
            start_url: Starting URL for the crawl
            max_pages: Maximum number of pages to crawl (default: 50)
            
        Returns:
            String containing all crawled content formatted as "url\ncontent\n\nurl\ncontent"
        """
        import requests
        import time
        import json
        
        # Set headers for all requests
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Step 1: Initiate the crawl
        crawl_data = {
            "start_url": start_url,
            "max_pages": max_pages
        }
        
        # Make the API request to initiate the crawl
        response = requests.post(f"{self.base_url}/crawls", headers=headers, json=crawl_data)
        
        # Check if the request was successful
        if response.status_code != 200:
            error_message = f"Error initiating crawl: {response.status_code} - {response.text}"
            raise Exception(error_message)
        
        # Get the crawl ID
        crawl_response = response.json()
        crawl_id = crawl_response.get("id")
        
        if not crawl_id:
            raise Exception("Failed to get crawl ID from response")
        
        # Step 2: Wait for the crawl to complete
        while True:
            # Get crawl information
            info_response = requests.get(f"{self.base_url}/crawls/{crawl_id}", headers=headers)
            
            if info_response.status_code != 200:
                error_message = f"Error checking crawl status: {info_response.status_code} - {info_response.text}"
                raise Exception(error_message)
            
            info = info_response.json()
            status = info.get("status")
            
            if status == "completed":
                break
            elif status == "failed":
                raise Exception(f"Crawl failed: {info.get('error', 'Unknown error')}")
            
            # Wait before checking again
            time.sleep(5)
        
        # Step 3: Get the list of crawled pages
        pages_response = requests.get(f"{self.base_url}/crawls/{crawl_id}/pages", headers=headers)
        
        if pages_response.status_code != 200:
            error_message = f"Error getting crawled pages: {pages_response.status_code} - {pages_response.text}"
            raise Exception(error_message)
        
        pages_data = pages_response.json()
        crawled_pages = pages_data.get("pages", [])
        
        # Step 4: Retrieve content for each page in parallel and format the output
        import concurrent.futures
        
        # Define a function to retrieve content for a single page
        def retrieve_page_content(page):
            url = page.get("url", "")
            retrieve_id = page.get("retrieve_id")
            
            if not url or not retrieve_id:
                return None
            
            # Retrieve content for this page
            params = {
                "retrieve_id": retrieve_id,
                "formats": json.dumps(["markdown"])
            }
            
            try:
                content_response = requests.get(f"{self.base_url}/retrieve", headers=headers, params=params)
                
                if content_response.status_code != 200:
                    print(f"Error retrieving content for {url}: {content_response.status_code} - {content_response.text}")
                    return None
                
                content_data = content_response.json()
                markdown_content = content_data.get("markdown_content", "")
                
                if url and markdown_content:
                    return {"url": url, "content": markdown_content}
                return None
            except Exception as e:
                print(f"Exception while retrieving content for {url}: {str(e)}")
                return None
        
        # Use ThreadPoolExecutor to retrieve content in parallel
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all tasks and create a future-to-page mapping
            future_to_page = {executor.submit(retrieve_page_content, page): page for page in crawled_pages}
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_page):
                result = future.result()
                if result:
                    results.append(result)
        
        # Sort results by URL to maintain a consistent order
        results.sort(key=lambda x: x["url"])
        
        # Format the output
        formatted_output = ""
        for result in results:
            if formatted_output:
                formatted_output += "\n\n"
            formatted_output += f"{result['url']}\n{result['content']}"
        
        return formatted_output


class FirecrawlSearchTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for FirecrawlSearchTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "requests": False,
            "firecrawl": False,
            "python-dotenv": False
        }
        
        # Check each dependency
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        try:
            import firecrawl
            dependencies["firecrawl"] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencies["python-dotenv"] = True
        except ImportError:
            pass
        
        return dependencies
    
    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Try to load the FIRECRAWL_API_KEY from a .env file using python-dotenv.
        
        Returns:
            The API key if found in .env file, None otherwise
        """
        try:
            # Try to import dotenv
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError("python-dotenv is not installed. Please install it with 'pip install python-dotenv'")
        
        # Check for .env file in current directory and parent directories
        current_dir = pathlib.Path.cwd()
        
        # Look in current directory and up to 3 parent directories
        for _ in range(4):
            env_path = current_dir / '.env'
            if env_path.exists():
                # Load the .env file
                load_dotenv(dotenv_path=env_path)
                
                # Check if FIRECRAWL_API_KEY is now in environment
                if "FIRECRAWL_API_KEY" in os.environ:
                    return os.environ["FIRECRAWL_API_KEY"]
            
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root directory
                break
            current_dir = parent_dir
        
        return None
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and API key is available.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
            EnvironmentError: If API key is not available
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("FirecrawlSearchTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        # Check if FIRECRAWL_API_KEY is set in environment variables
        if "FIRECRAWL_API_KEY" not in os.environ:
            try:
                # Try to load API key from .env file
                api_key = FirecrawlSearchTool._load_api_key_from_env_file()
                if api_key is None:
                    # Print missing API key message
                    missing_api_key("FirecrawlSearchTool", "FIRECRAWL_API_KEY")
                    raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and could not be found in .env file")
            except ImportError:
                # If dotenv is not installed, we can't load from .env file
                # Print missing API key message without dotenv support
                missing_api_key("FirecrawlSearchTool", "FIRECRAWL_API_KEY", dotenv_support=False)
                raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and python-dotenv is not installed")
        
        return True
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FirecrawlSearchTool.
        
        Args:
            api_key: Firecrawl API key (optional, will try to load from environment if not provided)
        """
        # Set API key
        self.api_key = api_key
        
        # If API key not provided, try to load from environment or .env file
        if self.api_key is None:
            # First check environment variables
            if "FIRECRAWL_API_KEY" in os.environ:
                self.api_key = os.environ["FIRECRAWL_API_KEY"]
            else:
                # Try to load from .env file
                try:
                    api_key = self._load_api_key_from_env_file()
                    if api_key:
                        self.api_key = api_key
                    else:
                        # Print missing API key message
                        missing_api_key("FirecrawlSearchTool", "FIRECRAWL_API_KEY")
                        raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and could not be found in .env file")
                except ImportError:
                    # If dotenv is not installed and no API key in environment
                    if "FIRECRAWL_API_KEY" not in os.environ:
                        # Print missing API key message without dotenv support
                        missing_api_key("FirecrawlSearchTool", "FIRECRAWL_API_KEY", dotenv_support=False)
                        raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and python-dotenv is not installed")
                    self.api_key = os.environ["FIRECRAWL_API_KEY"]
        
        # Initialize FirecrawlApp
        try:
            from firecrawl import FirecrawlApp
        except ImportError:
            missing_dependencies("FirecrawlSearchTool", ["firecrawl-py"])
            raise ImportError("firecrawl-py is not installed. Please install it with 'pip install firecrawl-py'")
    
    def search(self, query: str, limit: int = 5, tbs: Optional[str] = None, 
               lang: str = "en", country: str = "us", location: Optional[str] = None,
               timeout: int = 60000, scrape_options: Optional[Dict[str, Any]] = None) -> Any:
        """
        Search the web using Firecrawl API.
        
        Args:
            query: The search query
            limit: Maximum number of results to return (default: 5)
            tbs: Time-based search parameter
            lang: Language code for search results (default: 'en')
            country: Country code for search results (default: 'us')
            location: Location parameter for search results
            timeout: Timeout in milliseconds (default: 60000)
            scrape_options: Options for scraping search results
            
        Returns:
            Search results from Firecrawl
        """

        
        options = {
            
            "limit": limit,
            "tbs": tbs,
            "lang": lang,
            "country": country,
            "location": location,
            "timeout": timeout,
            "scrapeOptions": scrape_options or {},
        }
        from firecrawl import FirecrawlApp
        _firecrawl = FirecrawlApp(api_key=self.api_key)

        return _firecrawl.search(query=query, params=options)


class FirecrawlScrapeWebsiteTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for FirecrawlScrapeWebsiteTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "requests": False,
            "firecrawl": False,
            "python-dotenv": False
        }
        
        # Check each dependency
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        try:
            import firecrawl
            dependencies["firecrawl"] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencies["python-dotenv"] = True
        except ImportError:
            pass
        
        return dependencies
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and API key is available.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
            EnvironmentError: If API key is not available
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("FirecrawlScrapeWebsiteTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        # Check if FIRECRAWL_API_KEY is set in environment variables
        if "FIRECRAWL_API_KEY" not in os.environ:
            try:
                # Try to load API key from .env file
                api_key = FirecrawlScrapeWebsiteTool._load_api_key_from_env_file()
                if api_key is None:
                    # API key not found in .env file
                    missing_api_key("FirecrawlScrapeWebsiteTool", "FIRECRAWL_API_KEY")
                    raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and could not be found in .env file")
            except ImportError:
                # If dotenv is not installed, we can't load from .env file
                missing_api_key("FirecrawlScrapeWebsiteTool", "FIRECRAWL_API_KEY", dotenv_support=False)
                raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and python-dotenv is not installed")
        
        return True
    
    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Try to load the FIRECRAWL_API_KEY from a .env file using python-dotenv.
        
        Returns:
            The API key if found in .env file, None otherwise
        """
        try:
            # Try to import dotenv
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError("python-dotenv is not installed. Please install it with 'pip install python-dotenv'")
        
        # Check for .env file in current directory and parent directories
        current_dir = pathlib.Path.cwd()
        
        # Look in current directory and up to 3 parent directories
        for _ in range(4):
            env_path = current_dir / '.env'
            if env_path.exists():
                # Load the .env file
                load_dotenv(dotenv_path=env_path)
                
                # Check if FIRECRAWL_API_KEY is now in environment
                if "FIRECRAWL_API_KEY" in os.environ:
                    return os.environ["FIRECRAWL_API_KEY"]
            
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root directory
                break
            current_dir = parent_dir
        
        return None
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FirecrawlScrapeWebsiteTool.
        
        Args:
            api_key: Firecrawl API key (optional, will try to load from environment if not provided)
        """
        # Set API key
        self.api_key = api_key
        
        # If API key not provided, try to load from environment or .env file
        if self.api_key is None:
            # First check environment variables
            if "FIRECRAWL_API_KEY" in os.environ:
                self.api_key = os.environ["FIRECRAWL_API_KEY"]
            else:
                # Try to load from .env file
                try:
                    api_key = self._load_api_key_from_env_file()
                    if api_key:
                        self.api_key = api_key
                    else:
                        # Print missing API key message
                        missing_api_key("FirecrawlScrapeWebsiteTool", "FIRECRAWL_API_KEY")
                        raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and could not be found in .env file")
                except ImportError:
                    # If dotenv is not installed and no API key in environment
                    if "FIRECRAWL_API_KEY" not in os.environ:
                        # Print missing API key message without dotenv support
                        missing_api_key("FirecrawlScrapeWebsiteTool", "FIRECRAWL_API_KEY", dotenv_support=False)
                        raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and python-dotenv is not installed")
                    self.api_key = os.environ["FIRECRAWL_API_KEY"]
        
        # Initialize FirecrawlApp
        try:
            from firecrawl import FirecrawlApp
        except ImportError:
            raise ImportError("firecrawl-py is not installed. Please install it with 'pip install firecrawl-py'")
    
    def scrape_website(self, url: str, timeout: int = 30000, only_main_content: bool = True, 
                      formats: List[str] = None, include_tags: List[str] = None, 
                      exclude_tags: List[str] = None, headers: Dict[str, str] = None, 
                      wait_for: int = 0) -> Any:
        """
        Scrape a website using Firecrawl API.
        
        Args:
            url: Website URL to scrape
            timeout: Timeout in milliseconds (default: 30000)
            only_main_content: Whether to extract only the main content (default: True)
            formats: Output formats (default: ["markdown"])
            include_tags: HTML tags to include in the extraction
            exclude_tags: HTML tags to exclude from the extraction
            headers: Custom HTTP headers to use for the request
            wait_for: Time to wait for JavaScript execution in milliseconds
            
        Returns:
            Scraped content from the website
        """
        # Set default values
        if formats is None:
            formats = ["markdown"]
        if include_tags is None:
            include_tags = []
        if exclude_tags is None:
            exclude_tags = []
        if headers is None:
            headers = {}
        
        # Prepare scrape options
        options = {
            "formats": formats,
            "onlyMainContent": only_main_content,
            "includeTags": include_tags,
            "excludeTags": exclude_tags,
            "headers": headers,
            "waitFor": wait_for,
            "timeout": timeout,
        }
        
        # Initialize FirecrawlApp and scrape the URL
        from firecrawl import FirecrawlApp
        _firecrawl = FirecrawlApp(api_key=self.api_key)
        
        return _firecrawl.scrape_url(url, options)


class FirecrawlCrawlWebsiteTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for FirecrawlCrawlWebsiteTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "requests": False,
            "firecrawl": False,
            "python-dotenv": False
        }
        
        # Check each dependency
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        try:
            import firecrawl
            dependencies["firecrawl"] = True
        except ImportError:
            pass
        
        try:
            from dotenv import load_dotenv
            dependencies["python-dotenv"] = True
        except ImportError:
            pass
        
        return dependencies
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and API key is available.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
            EnvironmentError: If API key is not available
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("FirecrawlCrawlWebsiteTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        # Check if FIRECRAWL_API_KEY is set in environment variables
        if "FIRECRAWL_API_KEY" not in os.environ:
            try:
                # Try to load API key from .env file
                api_key = FirecrawlCrawlWebsiteTool._load_api_key_from_env_file()
                if api_key is None:
                    # API key not found in .env file
                    missing_api_key("FirecrawlCrawlWebsiteTool", "FIRECRAWL_API_KEY")
                    raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and could not be found in .env file")
            except ImportError:
                # If dotenv is not installed, we can't load from .env file
                missing_api_key("FirecrawlCrawlWebsiteTool", "FIRECRAWL_API_KEY", dotenv_support=False)
                raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and python-dotenv is not installed")
        
        return True
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FirecrawlCrawlWebsiteTool.
        
        Args:
            api_key: Firecrawl API key (optional, will try to load from environment if not provided)
        """
        # Set API key
        self.api_key = api_key
        
        # If API key not provided, try to load from environment or .env file
        if self.api_key is None:
            # First check environment variables
            if "FIRECRAWL_API_KEY" in os.environ:
                self.api_key = os.environ["FIRECRAWL_API_KEY"]
            else:
                # Try to load from .env file
                try:
                    api_key = self._load_api_key_from_env_file()
                    if api_key:
                        self.api_key = api_key
                    else:
                        # Print missing API key message
                        missing_api_key("FirecrawlCrawlWebsiteTool", "FIRECRAWL_API_KEY")
                        raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and could not be found in .env file")
                except ImportError:
                    # If dotenv is not installed and no API key in environment
                    if "FIRECRAWL_API_KEY" not in os.environ:
                        # Print missing API key message without dotenv support
                        missing_api_key("FirecrawlCrawlWebsiteTool", "FIRECRAWL_API_KEY", dotenv_support=False)
                        raise EnvironmentError("FIRECRAWL_API_KEY environment variable is not set and python-dotenv is not installed")
                    self.api_key = os.environ["FIRECRAWL_API_KEY"]
        
        # Initialize FirecrawlApp
        try:
            from firecrawl import FirecrawlApp
        except ImportError:
            raise ImportError("firecrawl-py is not installed. Please install it with 'pip install firecrawl-py'")
    
    def crawl_website(self, url: str, crawler_options: Dict[str, Any] = None, timeout: int = 30000) -> Any:
        """
        Crawl a website using Firecrawl API.
        
        Args:
            url: Website URL to crawl
            crawler_options: Options for crawling (default: {})
            timeout: Timeout in milliseconds (default: 30000)
            
        Returns:
            Crawled content from the website
        """
        # Set default values
        if crawler_options is None:
            crawler_options = {}
        
        # Prepare crawl options
        options = {
            "crawlerOptions": crawler_options,
            "timeout": timeout,
        }
        
        # Initialize FirecrawlApp and crawl the URL
        from firecrawl import FirecrawlApp
        _firecrawl = FirecrawlApp(api_key=self.api_key)
        
        return _firecrawl.crawl_url(url, options)

    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Try to load the FIRECRAWL_API_KEY from a .env file using python-dotenv.
        
        Returns:
            The API key if found in .env file, None otherwise
        """
        try:
            # Try to import dotenv
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError("python-dotenv is not installed. Please install it with 'pip install python-dotenv'")
        
        # Check for .env file in current directory and parent directories
        current_dir = pathlib.Path.cwd()
        
        # Look in current directory and up to 3 parent directories
        for _ in range(4):
            env_path = current_dir / '.env'
            if env_path.exists():
                # Load the .env file
                load_dotenv(dotenv_path=env_path)
                
                # Check if FIRECRAWL_API_KEY is now in environment
                if "FIRECRAWL_API_KEY" in os.environ:
                    return os.environ["FIRECRAWL_API_KEY"]
            
            # Move to parent directory
            parent_dir = current_dir.parent
            if parent_dir == current_dir:  # Reached root directory
                break
            current_dir = parent_dir
        
        return None

class YFinanceTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for YFinanceTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "yfinance": False,
            "pandas": False
        }
        
        # Check each dependency
        try:
            import yfinance
            dependencies["yfinance"] = True
        except ImportError:
            pass
        
        try:
            import pandas
            dependencies["pandas"] = True
        except ImportError:
            pass
        
        return dependencies
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and print missing ones.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("YFinanceTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        return True
    
    def __init__(self):
        """
        Initialize the YFinanceTool.
        """
        # Check if dependencies are installed
        self.__control__()
    
    def get_ticker_info(self, ticker: str) -> Dict[str, Any]:
        """
        Get basic information about a ticker.
        
        Args:
            ticker: The ticker symbol (e.g., 'AAPL' for Apple)
            
        Returns:
            Dictionary containing basic information about the ticker
        """
        import yfinance as yf
        
        # Get ticker object
        ticker_obj = yf.Ticker(ticker)
        
        # Get basic info
        info = ticker_obj.info
        
        return info
    
    def get_historical_data(self, ticker: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
        """
        Get historical market data for a ticker.
        
        Args:
            ticker: The ticker symbol (e.g., 'AAPL' for Apple)
            period: The period to fetch data for (default: '1mo')
                Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
            interval: The interval between data points (default: '1d')
                Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
            
        Returns:
            Dictionary containing historical data
        """
        import yfinance as yf
        import pandas as pd
        
        # Get ticker object
        ticker_obj = yf.Ticker(ticker)
        
        # Get historical data
        hist = ticker_obj.history(period=period, interval=interval)
        
        # Convert DataFrame to dictionary
        hist_dict = hist.reset_index().to_dict(orient='records')
        
        return {
            "data": hist_dict,
            "period": period,
            "interval": interval,
            "ticker": ticker
        }
    
    def get_financials(self, ticker: str) -> Dict[str, Any]:
        """
        Get financial statements for a ticker.
        
        Args:
            ticker: The ticker symbol (e.g., 'AAPL' for Apple)
            
        Returns:
            Dictionary containing financial statements
        """
        import yfinance as yf
        import pandas as pd
        
        # Get ticker object
        ticker_obj = yf.Ticker(ticker)
        
        # Get financial statements
        income_stmt = ticker_obj.income_stmt
        balance_sheet = ticker_obj.balance_sheet
        cash_flow = ticker_obj.cashflow
        
        # Convert DataFrames to dictionaries
        income_stmt_dict = income_stmt.reset_index().to_dict(orient='records') if not income_stmt.empty else []
        balance_sheet_dict = balance_sheet.reset_index().to_dict(orient='records') if not balance_sheet.empty else []
        cash_flow_dict = cash_flow.reset_index().to_dict(orient='records') if not cash_flow.empty else []
        
        return {
            "income_statement": income_stmt_dict,
            "balance_sheet": balance_sheet_dict,
            "cash_flow": cash_flow_dict,
            "ticker": ticker
        }
    
    def search_tickers(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        Search for ticker symbols based on a query.
        
        Args:
            query: The search query (e.g., 'Apple')
            limit: Maximum number of results to return (default: 10)
            
        Returns:
            List of dictionaries containing ticker symbols and company names
        """
        import yfinance as yf
        
        try:
            # Use yfinance's search functionality
            tickers = yf.Tickers(query)
            
            # Get the tickers that were found
            found_tickers = list(tickers.tickers.keys())
            
            # Limit the number of results
            found_tickers = found_tickers[:limit]
            
            # Get info for each ticker
            result = []
            for ticker_symbol in found_tickers:
                try:
                    ticker_obj = yf.Ticker(ticker_symbol)
                    info = ticker_obj.info
                    result.append({
                        "symbol": ticker_symbol,
                        "name": info.get("shortName", "Unknown"),
                        "exchange": info.get("exchange", "Unknown"),
                        "industry": info.get("industry", "Unknown")
                    })
                except Exception as e:
                    # Skip tickers that cause errors
                    continue
            
            return result
        except Exception as e:
            # If the search fails, return an empty list
            return []


class ArxivTool:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for ArxivTool and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "arxiv": False,
            "requests": False,
            "PyPDF2": False
        }
        
        # Check each dependency
        try:
            import arxiv
            dependencies["arxiv"] = True
        except ImportError:
            pass
        
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        try:
            import PyPDF2
            dependencies["PyPDF2"] = True
        except ImportError:
            pass
        
        return dependencies
    
    def __control__(self) -> bool:
        """
        Check if the required dependencies are installed and print missing ones.
        
        Returns:
            True if all requirements are met
        
        Raises:
            ImportError: If required packages are not installed
        """
        # Analyze dependencies
        dependencies = self.analyze_dependencies()
        missing = [dep for dep, installed in dependencies.items() if not installed]
        
        # Print missing dependencies
        if missing:
            # Use the new printing function
            missing_dependencies("ArxivTool", missing)
            
            # Raise ImportError with combined message for all missing dependencies
            install_cmd = "pip install " + " ".join(missing)
            raise ImportError(f"Missing dependencies: {', '.join(missing)}. Please install them with: {install_cmd}")
        
        return True
    
    def __init__(self):
        """
        Initialize the ArxivTool.
        """
        # Check if dependencies are installed
        self.__control__()
    
    def search(self, query: str, max_results: int = 5, sort_by: str = "relevance", sort_order: str = "descending") -> List[Dict[str, Any]]:
        """
        Search for papers on arXiv.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return (default: 5)
            sort_by: Sort results by 'relevance', 'lastUpdatedDate', or 'submittedDate' (default: 'relevance')
            sort_order: Sort order, either 'ascending' or 'descending' (default: 'descending')
            
        Returns:
            List of dictionaries containing paper information
        """
        import arxiv
        
        # Map sort_by to arxiv.SortCriterion
        sort_criteria = {
            "relevance": arxiv.SortCriterion.Relevance,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
            "submittedDate": arxiv.SortCriterion.SubmittedDate
        }
        
        # Map sort_order to arxiv.SortOrder
        sort_orders = {
            "ascending": arxiv.SortOrder.Ascending,
            "descending": arxiv.SortOrder.Descending
        }
        
        # Set default values if invalid options are provided
        if sort_by not in sort_criteria:
            sort_by = "relevance"
        if sort_order not in sort_orders:
            sort_order = "descending"
        
        # Create search client
        client = arxiv.Client()
        
        # Create search query
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criteria[sort_by],
            sort_order=sort_orders[sort_order]
        )
        
        # Execute search
        results = list(client.results(search))
        
        # Convert results to dictionaries
        papers = []
        for paper in results:
            papers.append({
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "summary": paper.summary,
                "published": paper.published.strftime("%Y-%m-%d") if paper.published else None,
                "updated": paper.updated.strftime("%Y-%m-%d") if paper.updated else None,
                "doi": paper.doi,
                "primary_category": paper.primary_category,
                "categories": paper.categories,
                "links": [link.href for link in paper.links],
                "pdf_url": paper.pdf_url,
                "entry_id": paper.entry_id
            })
        
        return papers
    
    def get_paper_by_id(self, paper_id: str) -> Dict[str, Any]:
        """
        Get a specific paper by its arXiv ID.
        
        Args:
            paper_id: The arXiv ID of the paper (e.g., '2106.09685')
            
        Returns:
            Dictionary containing paper information
        """
        import arxiv
        
        # Create client
        client = arxiv.Client()
        
        # Search for the specific paper
        search = arxiv.Search(id_list=[paper_id])
        
        # Get the paper
        results = list(client.results(search))
        
        if not results:
            return {"error": f"Paper with ID {paper_id} not found"}
        
        paper = results[0]
        
        # Convert to dictionary
        paper_dict = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "published": paper.published.strftime("%Y-%m-%d") if paper.published else None,
            "updated": paper.updated.strftime("%Y-%m-%d") if paper.updated else None,
            "doi": paper.doi,
            "primary_category": paper.primary_category,
            "categories": paper.categories,
            "links": [link.href for link in paper.links],
            "pdf_url": paper.pdf_url,
            "entry_id": paper.entry_id
        }
        
        return paper_dict
    
    def download_paper(self, paper_id: str, output_dir: str = "./") -> Dict[str, Any]:
        """
        Download a paper's PDF by its arXiv ID.
        
        Args:
            paper_id: The arXiv ID of the paper (e.g., '2106.09685')
            output_dir: Directory to save the PDF (default: current directory)
            
        Returns:
            Dictionary containing download information
        """
        import arxiv
        import os
        import requests
        
        # Create client
        client = arxiv.Client()
        
        # Search for the specific paper
        search = arxiv.Search(id_list=[paper_id])
        
        # Get the paper
        results = list(client.results(search))
        
        if not results:
            return {"error": f"Paper with ID {paper_id} not found"}
        
        paper = results[0]
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        filename = f"{paper_id.replace('/', '_')}.pdf"
        filepath = os.path.join(output_dir, filename)
        
        # Download the PDF
        try:
            response = requests.get(paper.pdf_url)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return {
                "success": True,
                "paper_id": paper_id,
                "title": paper.title,
                "filepath": filepath,
                "pdf_url": paper.pdf_url
            }
        except Exception as e:
            return {
                "success": False,
                "paper_id": paper_id,
                "error": str(e),
                "pdf_url": paper.pdf_url
            }
    
    def read_paper(self, paper_id: str, max_pages: int = None) -> Dict[str, Any]:
        """
        Read a paper's content directly by its arXiv ID.
        
        Args:
            paper_id: The arXiv ID of the paper (e.g., '2106.09685')
            max_pages: Maximum number of pages to read (default: None, reads all pages)
            
        Returns:
            Dictionary containing the paper's content and metadata
        """
        import arxiv
        import requests
        import tempfile
        import os
        import PyPDF2
        
        # Create client
        client = arxiv.Client()
        
        # Search for the specific paper
        search = arxiv.Search(id_list=[paper_id])
        
        # Get the paper
        results = list(client.results(search))
        
        if not results:
            return {"error": f"Paper with ID {paper_id} not found"}
        
        paper = results[0]
        
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate filename
            filename = f"{paper_id.replace('/', '_')}.pdf"
            filepath = os.path.join(temp_dir, filename)
            
            # Download the PDF
            try:
                response = requests.get(paper.pdf_url)
                response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Read the PDF content
                with open(filepath, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    
                    # Get number of pages
                    num_pages = len(pdf_reader.pages)
                    
                    # Limit pages if max_pages is specified
                    if max_pages is not None:
                        num_pages = min(num_pages, max_pages)
                    
                    # Extract text from pages with better handling
                    content = []
                    for page_num in range(num_pages):
                        try:
                            page = pdf_reader.pages[page_num]
                            page_text = page.extract_text()
                            
                            # Skip empty pages or pages with very little content
                            if page_text and len(page_text.strip()) > 20:
                                # Clean up the text
                                page_text = page_text.replace('\n\n', '\n')
                                content.append(f"--- Page {page_num + 1} ---\n{page_text}")
                        except Exception as e:
                            content.append(f"--- Page {page_num + 1} ---\n[Error extracting text: {str(e)}]")
                    
                    # Join all pages with clear separation
                    full_content = "\n\n".join(content)
                    
                    # If we couldn't extract meaningful content, try an alternative approach
                    if not full_content or len(full_content.strip()) < 100:
                        try:
                            # Alternative extraction method
                            full_content = "Content could not be extracted properly. Please try downloading the paper directly."
                            
                            # Include the abstract as a fallback
                            full_content = f"Abstract:\n{paper.summary}\n\n{full_content}"
                        except Exception:
                            full_content = "Failed to extract content from the PDF. Please download the paper directly."
                
                return {
                    "success": True,
                    "paper_id": paper_id,
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary,
                    "content": full_content,
                    "total_pages": len(pdf_reader.pages),
                    "pages_read": num_pages,
                    "pdf_url": paper.pdf_url
                }
            except Exception as e:
                # If we failed to process the PDF, return the summary at least
                return {
                    "success": False,
                    "paper_id": paper_id,
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary,
                    "error": str(e),
                    "pdf_url": paper.pdf_url,
                    "note": "Failed to extract content. You can still access the paper directly using the pdf_url."
                }


class YouTubeVideo:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for YouTubeVideo and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "youtube_transcript_api": False
        }
        
        # Check each dependency
        try:
            import youtube_transcript_api
            dependencies["youtube_transcript_api"] = True
        except ImportError:
            pass
        
        return dependencies
        
    @staticmethod
    def __control__() -> bool:
        # Check the import youtube_transcript_api
        try:
            import youtube_transcript_api
            return True
        except ImportError:
            # Use the missing_dependencies function to display the error
            missing_dependencies("YouTubeVideo", ["youtube_transcript_api"])
            raise ImportError("Missing dependency: youtube_transcript_api. Please install it with: pip install youtube_transcript_api")
    
    @staticmethod
    def get_video_id(url: str) -> Optional[str]:
        """
        Extract the YouTube video ID from a URL.
        
        Args:
            url: The URL of the YouTube video
            
        Returns:
            The video ID or None if not found
        """
        import re
        from urllib.parse import urlparse, parse_qs
        
        # Handle different YouTube URL formats
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        
        if hostname == "youtu.be":
            return parsed_url.path[1:]
        
        if hostname in ("www.youtube.com", "youtube.com"):
            if parsed_url.path == "/watch":
                query_params = parse_qs(parsed_url.query)
                return query_params.get("v", [None])[0]
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            if parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]
        
        # Try to extract ID using regex as fallback
        youtube_regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(youtube_regex, url)
        if match:
            return match.group(1)
            
        return None
    
    @staticmethod
    def get_captions(url: str, languages: List[str] = None) -> str:
        """
        Get captions/transcript from a YouTube video.
        
        Args:
            url: The URL of the YouTube video
            languages: List of language codes to try (default: ["en"])
            
        Returns:
            The video transcript as text
        """
        from youtube_transcript_api import YouTubeTranscriptApi
        
        # Default to English if no languages specified
        if not languages:
            languages = ["en"]
            
        video_id = YouTubeVideo.get_video_id(url)
        if not video_id:
            return "Error: Could not extract video ID from URL"
            
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return " ".join(line["text"] for line in transcript)
        except Exception as e:
            return f"Error getting captions: {str(e)}"
    
    @staticmethod
    def get_video_data(url: str) -> Dict[str, Any]:
        """
        Get metadata about a YouTube video.
        
        Args:
            url: The URL of the YouTube video
            
        Returns:
            Dictionary containing video metadata
        """
        import json
        from urllib.request import urlopen
        from urllib.parse import urlencode
        
        video_id = YouTubeVideo.get_video_id(url)
        if not video_id:
            return {"error": "Could not extract video ID from URL"}
            
        try:
            params = {"format": "json", "url": f"https://www.youtube.com/watch?v={video_id}"}
            oembed_url = "https://www.youtube.com/oembed"
            query_string = urlencode(params)
            full_url = f"{oembed_url}?{query_string}"
            
            with urlopen(full_url) as response:
                response_text = response.read()
                video_data = json.loads(response_text.decode())
                
                return {
                    "title": video_data.get("title"),
                    "author_name": video_data.get("author_name"),
                    "author_url": video_data.get("author_url"),
                    "type": video_data.get("type"),
                    "height": video_data.get("height"),
                    "width": video_data.get("width"),
                    "version": video_data.get("version"),
                    "provider_name": video_data.get("provider_name"),
                    "provider_url": video_data.get("provider_url"),
                    "thumbnail_url": video_data.get("thumbnail_url"),
                    "video_id": video_id,
                    "video_url": f"https://www.youtube.com/watch?v={video_id}"
                }
        except Exception as e:
            return {"error": f"Error getting video data: {str(e)}"}
    
    @staticmethod
    def get_timestamps(url: str, languages: List[str] = None) -> str:
        """
        Generate timestamps with captions for a YouTube video.
        
        Args:
            url: The URL of the YouTube video
            languages: List of language codes to try (default: ["en"])
            
        Returns:
            Formatted timestamps with captions
        """
        from youtube_transcript_api import YouTubeTranscriptApi
        
        # Default to English if no languages specified
        if not languages:
            languages = ["en"]
            
        video_id = YouTubeVideo.get_video_id(url)
        if not video_id:
            return "Error: Could not extract video ID from URL"
            
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            
            timestamps = []
            for line in transcript:
                start_seconds = int(line["start"])
                minutes, seconds = divmod(start_seconds, 60)
                hours, minutes = divmod(minutes, 60)
                
                if hours > 0:
                    time_str = f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    time_str = f"{minutes}:{seconds:02d}"
                    
                timestamps.append(f"{time_str} - {line['text']}")
                
            return "\n".join(timestamps)
        except Exception as e:
            return f"Error generating timestamps: {str(e)}"


class YoutubeSearch:
    @staticmethod
    def _load_api_key_from_env_file() -> Optional[str]:
        """
        Load the Serper API key from the .env file.
        
        Returns:
            The API key if found, None otherwise
        """
        try:
            # Try to load from .env file
            env_path = pathlib.Path('.env')
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.strip().startswith('SERPER_API_KEY='):
                            api_key = line.strip().split('=', 1)[1].strip()
                            # Remove quotes if present
                            if (api_key.startswith('"') and api_key.endswith('"')) or \
                               (api_key.startswith("'") and api_key.endswith("'")):
                                api_key = api_key[1:-1]
                            return api_key
        except Exception:
            pass
        return None
    
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for YoutubeSearch and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "requests": False
        }
        
        # Check each dependency
        try:
            import requests
            dependencies["requests"] = True
        except ImportError:
            pass
        
        return dependencies
    
    def __control__(self) -> bool:
        # Check if requests is installed
        try:
            import requests
            return True
        except ImportError:
            # Use the missing_dependencies function to display the error
            missing_dependencies("YoutubeSearch", ["requests"])
            raise ImportError("Missing dependency: requests. Please install it with: pip install requests")
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the YoutubeSearch tool.
        
        Args:
            api_key: The Serper API key. If not provided, will try to load from environment or .env file.
        """
        # Check dependencies
        self.__control__()
        
        # Set API key
        self.api_key = api_key
        
        # If API key is not provided, try to get it from environment variable
        if self.api_key is None:
            import os
            self.api_key = os.environ.get("SERPER_API_KEY")
            
        # If still not found, try to load from .env file
        if self.api_key is None:
            self.api_key = self._load_api_key_from_env_file()
            
        # If still not found, raise error
        if self.api_key is None:
            missing_api_key("YoutubeSearch", "SERPER_API_KEY")
            raise ValueError("Serper API key not found. Please provide it as an argument, set it as an environment variable, or add it to your .env file.")
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos using the Serper API.
        
        Args:
            query: The search query
            limit: Maximum number of results to return (default: 5)
            
        Returns:
            List of video results with metadata
        """
        import requests
        import json
        
        url = "https://google.serper.dev/videos"
        
        payload = {
            "q": query,
            "gl": "us",
            "hl": "en"
        }
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Process and clean up the results
            videos = []
            
            # Check if 'videos' key exists in the response
            if "videos" in data:
                for video in data["videos"][:limit]:
                    # Handle channel data safely
                    channel_name = ""
                    channel_link = ""
                    
                    if "channel" in video:
                        if isinstance(video["channel"], dict):
                            channel_name = video["channel"].get("name", "")
                            channel_link = video["channel"].get("link", "")
                    
                    processed_video = {
                        "title": video.get("title", ""),
                        "link": video.get("link", ""),
                        "thumbnail": video.get("thumbnail", ""),
                        "channel": channel_name,
                        "channel_link": channel_link,
                        "date_published": video.get("date", ""),
                        "views": video.get("views", ""),
                        "description": video.get("description", ""),
                        "duration": video.get("duration", "")
                    }
                    videos.append(processed_video)
            else:
                # Try to extract videos from a different key if available
                if "organic" in data:
                    for item in data["organic"][:limit]:
                        if "link" in item and ("youtube.com" in item.get("link", "") or "youtu.be" in item.get("link", "")):
                            videos.append({
                                "title": item.get("title", ""),
                                "link": item.get("link", ""),
                                "thumbnail": item.get("thumbnail", ""),
                                "description": item.get("snippet", "")
                            })
            
            if not videos:
                return [{"message": "No YouTube videos found for the query"}]
            
            return videos
        except Exception as e:
            return [{"error": f"Error searching YouTube videos: {str(e)}"}]


class Crawl4AISimpleCrawling:
    @staticmethod
    def analyze_dependencies() -> Dict[str, bool]:
        """
        Analyze the dependencies required for Crawl4AISimpleCrawling and return their status.
        
        Returns:
            Dictionary with dependency names as keys and their availability status as values
        """
        dependencies = {
            "crawl4ai": False,
            "asyncio": False
        }
        
        # Check each dependency
        try:
            import crawl4ai
            dependencies["crawl4ai"] = True
        except ImportError:
            pass
            
        try:
            import asyncio
            dependencies["asyncio"] = True
        except ImportError:
            pass
        
        return dependencies
    
    def __control__(self) -> bool:
        # Check if required packages are installed
        try:
            import crawl4ai
            import asyncio
            return True
        except ImportError as e:
            missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
            # Use the missing_dependencies function to display the error
            missing_dependencies("Crawl4AISimpleCrawling", ["crawl4ai", "asyncio"])
            raise ImportError(f"Missing dependency: {missing_module}. Please install it with: pip install crawl4ai")
    
    def __init__(self):
        """
        Initialize the Crawl4AISimpleCrawling tool.
        """
        # Check dependencies
        self.__control__()
    
    def crawl(self, url: str, browser_config: Dict[str, Any] = None, run_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Crawl a website and extract its content using Crawl4AI.
        
        Args:
            url: The URL to crawl
            browser_config: Optional browser configuration parameters
            run_config: Optional crawler run configuration parameters
            
        Returns:
            Dictionary containing the crawled content and metadata
        """
        try:
            import asyncio
            from crawl4ai import AsyncWebCrawler
            from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
            
            # Create a synchronous wrapper for the async crawling function
            def sync_crawl(url, browser_config=None, run_config=None):
                async def _crawl():
                    # Initialize configs with defaults or provided values
                    browser_cfg = BrowserConfig(**(browser_config or {}))
                    run_cfg = CrawlerRunConfig(**(run_config or {}))
                    
                    async with AsyncWebCrawler(config=browser_cfg) as crawler:
                        result = await crawler.arun(url=url, config=run_cfg)
                        return {
                            "raw_markdown": result.markdown.raw_markdown,
                            "media": result.media,
                            "links": result.links,
                        }
                
                return asyncio.run(_crawl())
            
            # Execute the synchronous wrapper
            result = sync_crawl(url, browser_config, run_config)
            return result
            
        except Exception as e:
            return {"error": f"Error crawling website: {str(e)}"}


# Export all tool classes
__all__ = ["Search", "ComputerUse", "BrowserUse", "Wikipedia", "DuckDuckGo", "SerperDev", "OlostepWebSearchTool", "OlostepScrapeWebsiteTool", "OlostepCrawlWebsiteTool", "FirecrawlSearchTool", "FirecrawlScrapeWebsiteTool", "FirecrawlCrawlWebsiteTool", "YFinanceTool", "ArxivTool", "YouTubeVideo", "YoutubeSearch", "Crawl4AISimpleCrawling"] 
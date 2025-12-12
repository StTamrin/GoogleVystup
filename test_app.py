import unittest
from unittest.mock import patch, MagicMock
from app import app


class SearchApiTestCase(unittest.TestCase):
    def setUp(self):
        # Flask testovací klient
        self.client = app.test_client()

    def test_search_missing_query_returns_400(self):
        """Když chybí parametr q, má vrátit 400."""
        resp = self.client.get("/api/search")
        self.assertEqual(resp.status_code, 400)

        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("Missing query", data["error"])

    @patch("app.requests.get")
    def test_search_returns_results_from_google_api(self, mock_get):
        """
        Otestujeme, že endpoint správně zpracuje odpověď z Google API.
        Volání requests.get se tady NESPUSTÍ do internetu – jen vrátí náš fake.
        """
        # připravíme falešnou odpověď Google API
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = {
            "items": [
                {
                    "title": "Example result",
                    "link": "https://example.com",
                    "snippet": "Some example snippet.",
                }
            ]
        }
        mock_get.return_value = fake_response

        # zavoláme náš endpoint
        resp = self.client.get("/api/search?q=sett")
        self.assertEqual(resp.status_code, 200)

        data = resp.get_json()
        # základní struktura
        self.assertIn("query", data)
        self.assertIn("count", data)
        self.assertIn("results", data)

        # měla by být 1 položka, podle fake_response
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)

        result = data["results"][0]
        self.assertEqual(result["title"], "Example result")
        self.assertEqual(result["link"], "https://example.com")
        self.assertEqual(result["snippet"], "Some example snippet.")


if __name__ == "__main__":
    unittest.main()
import pytest
from datetime import date, timedelta

PRODUCT_SAMPLE = {
    "description": "Produto Teste",
    "price": 49.99,
    "barcode": "1234567890123",
    "section": "Roupas",
    "stock": 10,
    "expiration_date": (date.today() + timedelta(days=30)).isoformat(),
}

PRODUCT_DUPLICATE = {
    "description": "Produto Duplicado",
    "price": 59.99,
    "barcode": "1234567890123",
    "section": "Eletrônicos",
    "stock": 5,
}

PRODUCT_UPDATE = {
    "price": 59.99,
    "stock": 20,
}

@pytest.fixture
def auth_headers(token_admin):
    return {"Authorization": f"Bearer {token_admin}"}


class TestProductBusinessRules:

    def test_list_products_with_pagination_and_filters(self, client, auth_headers):
        # Assumindo que tem vários produtos no banco (ou crie alguns fixtures antes)
        params = {
            "section": "Roupas",
            "min_price": 40,
            "max_price": 100,
            "available": True,
            "page": 1,
            "limit": 10,
        }
        response = client.get("/products/", headers=auth_headers, params=params)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list) or "items" in data  # Depende do seu retorno paginado
        # Checar se os produtos retornados batem com os filtros (exemplo básico)
        for product in data.get("items", data):  
            assert product["section"] == "Roupas"
            assert 40 <= product["price"] <= 100
            assert product["stock"] > 0

    def test_create_product_success(self, client, auth_headers):
        response = client.post("/products/", json=PRODUCT_SAMPLE, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["barcode"] == PRODUCT_SAMPLE["barcode"]
        assert data["expiration_date"] == PRODUCT_SAMPLE["expiration_date"]

    def test_create_product_duplicate_barcode(self, client, auth_headers):
        # Cria primeiro produto
        client.post("/products/", json=PRODUCT_SAMPLE, headers=auth_headers)
        # Tenta criar produto com mesmo barcode
        response = client.post("/products/", json=PRODUCT_DUPLICATE, headers=auth_headers)
        assert response.status_code in (400, 409)

    def test_get_product_not_found(self, client, auth_headers):
        response = client.get("/products/9999999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_product_success(self, client, auth_headers):
        create_resp = client.post("/products/", json=PRODUCT_SAMPLE, headers=auth_headers)
        product_id = create_resp.json()["id"]

        response = client.put(f"/products/{product_id}", json=PRODUCT_UPDATE, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == PRODUCT_UPDATE["price"]
        assert data["stock"] == PRODUCT_UPDATE["stock"]

    def test_update_product_not_found(self, client, auth_headers):
        response = client.put("/products/9999999", json=PRODUCT_UPDATE, headers=auth_headers)
        assert response.status_code == 404

    def test_delete_product_success(self, client, auth_headers):
        create_resp = client.post("/products/", json=PRODUCT_SAMPLE, headers=auth_headers)
        product_id = create_resp.json()["id"]

        response = client.delete(f"/products/{product_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json().get("detail") == "Produto deletado com sucesso"

    def test_delete_product_not_found(self, client, auth_headers):
        response = client.delete("/products/9999999", headers=auth_headers)
        assert response.status_code == 404

    def test_create_product_invalid_expiration_date(self, client, auth_headers):
        invalid_product = PRODUCT_SAMPLE.copy()
        invalid_product["expiration_date"] = "invalid-date-format"
        response = client.post("/products/", json=invalid_product, headers=auth_headers)
        assert response.status_code == 422

    def test_create_product_invalid_images(self, client, auth_headers):
        invalid_product = PRODUCT_SAMPLE.copy()
        invalid_product["images"] = ["not-a-url"]
        response = client.post("/products/", json=invalid_product, headers=auth_headers)
        assert response.status_code == 422


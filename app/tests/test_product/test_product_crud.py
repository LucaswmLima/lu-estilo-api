import pytest

INVALID_PRODUCTS = [
    # descrição vazia
    {"description": "", "price": 10.0, "barcode": "0000000000001", "section": "Roupas", "stock": 5},
    # preço negativo
    {"description": "Teste", "price": -5.0, "barcode": "0000000000002", "section": "Roupas", "stock": 5},
    # barcode vazio
    {"description": "Teste", "price": 10.0, "barcode": "", "section": "Roupas", "stock": 5},
    # estoque negativo
    {"description": "Teste", "price": 10.0, "barcode": "0000000000003", "section": "Roupas", "stock": -1},
]

class TestAdminCrudValidations:
    @pytest.fixture(autouse=True)
    def setup_headers(self, token_admin):
        self.headers = {"Authorization": f"Bearer {token_admin}"}

    def test_create_product_with_invalid_data(self, client):
        for invalid_product in INVALID_PRODUCTS:
            response = client.post("/products/", json=invalid_product, headers=self.headers)
            assert response.status_code == 422

    def test_create_product_duplicate_barcode(self, client, create_test_product):
        # tentar criar um produto com barcode já existente (do create_test_product)
        product_data = {
            "description": "Outro Produto",
            "price": 20.0,
            "barcode": create_test_product.barcode,
            "section": "Eletrônicos",
            "stock": 10,
        }
        response = client.post("/products/", json=product_data, headers=self.headers)
        assert response.status_code == 400
        assert "barcode" in response.json()["detail"].lower()

    def test_update_product_with_invalid_data(self, client, create_test_product):
        for invalid_data in [
            {"price": -10},
            {"description": ""},
            {"stock": -5},
            {"barcode": ""}
        ]:
            response = client.put(f"/products/{create_test_product.id}", json=invalid_data, headers=self.headers)
            assert response.status_code == 422

    def test_update_product_duplicate_barcode(self, client, create_test_product):
        # cria um outro produto com barcode diferente
        product_data = {
            "description": "Produto Extra",
            "price": 15.0,
            "barcode": "9999999999999",
            "section": "Roupas",
            "stock": 8,
        }
        res = client.post("/products/", json=product_data, headers=self.headers)
        assert res.status_code == 200
        new_product_id = res.json()["id"]

        # tenta atualizar o novo produto com barcode do create_test_product (duplicado)
        response = client.put(
            f"/products/{new_product_id}",
            json={"barcode": create_test_product.barcode},
            headers=self.headers
        )
        assert response.status_code == 400
        assert "barcode" in response.json()["detail"].lower()

    def test_delete_nonexistent_product_returns_404(self, client):
        response = client.delete("/products/9999999", headers=self.headers)
        assert response.status_code == 404

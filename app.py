from flask import Flask, jsonify, request
import store
import external_api


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify({"message": "Inventory Management API is running"})

    # -----------------------------
    # CRUD ROUTES
    # -----------------------------

    @app.route("/inventory", methods=["GET"])
    def get_inventory():
        return jsonify(store.get_all_items()), 200

    @app.route("/inventory/<int:item_id>", methods=["GET"])
    def get_inventory_item(item_id):
        item = store.get_item_by_id(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item), 200

    @app.route("/inventory", methods=["POST"])
    def create_inventory_item():
        data = request.get_json() or {}

        required_fields = ["name", "price", "stock"]
        missing = [field for field in required_fields if field not in data]

        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        item = {
            "id": store.get_next_id(),
            "name": data["name"],
            "brand": data.get("brand", ""),
            "barcode": data.get("barcode", ""),
            "price": data["price"],
            "stock": data["stock"],
            "ingredients": data.get("ingredients", ""),
            "category": data.get("category", "")
        }

        store.add_item(item)
        return jsonify(item), 201

    @app.route("/inventory/<int:item_id>", methods=["PATCH"])
    def patch_inventory_item(item_id):
        data = request.get_json() or {}
        item = store.update_item(item_id, data)

        if not item:
            return jsonify({"error": "Item not found"}), 404

        return jsonify(item), 200

    @app.route("/inventory/<int:item_id>", methods=["DELETE"])
    def delete_inventory_item(item_id):
        deleted = store.delete_item(item_id)

        if not deleted:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Item deleted", "item": deleted}), 200

    # -----------------------------
    # EXTERNAL API ROUTES
    # -----------------------------

    @app.route("/external/product", methods=["GET"])
    def fetch_external_product():
        barcode = request.args.get("barcode")

        if not barcode:
            return jsonify({"error": "barcode query parameter is required"}), 400

        try:
            product = external_api.get_product_by_barcode(barcode)
            if not product:
                return jsonify({"error": "Product not found in external API"}), 404
            return jsonify(product), 200
        except Exception as e:
            return jsonify({"error": f"External API failed: {str(e)}"}), 500

    @app.route("/external/search", methods=["GET"])
    def search_external_products():
        name = request.args.get("name")

        if not name:
            return jsonify({"error": "name query parameter is required"}), 400

        try:
            products = external_api.search_products_by_name(name)
            return jsonify(products), 200
        except Exception as e:
            return jsonify({"error": f"External API failed: {str(e)}"}), 500

    @app.route("/inventory/from-external", methods=["POST"])
    def add_from_external():
        data = request.get_json() or {}
        barcode = data.get("barcode")

        if not barcode:
            return jsonify({"error": "barcode is required"}), 400

        try:
            product = external_api.get_product_by_barcode(barcode)
            if not product:
                return jsonify({"error": "Product not found in external API"}), 404

            item = {
                "id": store.get_next_id(),
                "name": product["name"],
                "brand": product["brand"],
                "barcode": product["barcode"],
                "price": data.get("price", 0.0),
                "stock": data.get("stock", 0),
                "ingredients": product["ingredients"],
                "category": product["category"]
            }

            store.add_item(item)
            return jsonify(item), 201

        except Exception as e:
            return jsonify({"error": f"External API failed: {str(e)}"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
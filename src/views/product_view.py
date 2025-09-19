from controllers.product_controller import ProductController

class ProductView:
    def __init__(self):
        self.controller = ProductController()

    def show_options(self):
        while True:
            print("\n===== PRODUITS =====")
            print("1. Montrer la liste d'items")
            print("2. Ajouter un item")
            print("3. Supprimer un item (facultatif)")
            print("4. Retour")
            choice = input("Choisissez une option: ").strip()

            if choice == "1":
                products = self.controller.list_products()
                if not products:
                    print("(aucun produit)")
                else:
                    for p in products:
                        print(f"{p.id}: {p.name} | {p.brand} | ${p.price:.2f}")

            elif choice == "2":
                name  = input("Nom: ").strip()
                brand = input("Marque: ").strip()
                price = float(input("Prix: ").strip())
                new_id = self.controller.add_product(name, brand, price)
                print(f"Ajouté avec id={new_id}")

            elif choice == "3":
                pid = int(input("Id à supprimer: ").strip())
                ok = self.controller.delete_product(pid)
                print("Supprimé" if ok else "Introuvable")

            elif choice == "4":
                break
            else:
                print("Option invalide.")

from fpdf import FPDF
import pandas

df = pandas.read_csv("articles.csv", dtype={"id":str})

class Article:
    def __init__(self,article_id):
        self.id = article_id
        self.name = df.loc[df['id'] == self.id,'name'].squeeze()
        self.price = df.loc[df['id'] == self.id, 'price'].squeeze()

    def available(self):
        in_stock = df.loc[df['id'] == self.id,'in stock'].squeeze()
        return in_stock

class Receipt:
    def __init__(self,article):
        self.article = article

    def generate(self):

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.1", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: Laptop Sven", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: 999", ln=1)

        pdf.output("receipt.pdf")

print(df)
article_id = input("Choose an article ID:")
article = Article(article_id=article_id)
if article.available():
    receipt = Receipt(article)
    receipt.generate()
else:
    print("No such article in stock")



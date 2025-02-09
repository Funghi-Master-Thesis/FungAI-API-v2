import os
import pandas as pd
import matplotlib.pyplot as plt

# Data for genus
genus_list = [
    "Penicillium", "Penicilluim", "Penicilluim", "Aspergillus", "Aspergillus",
    "Aspergillus", "Cladosporium", "Rhizomucor", "Hypocrea", "Hamigera",
    "Acremonium", "Epicoccum", "Epicoccum", "Epicoccum", "Aureobasidium",
    "Pesisa", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Penicillium", "Penicillium", "Aspergillus", "Talaromyces",
    "Aspergillus", "Fusarium", "Fusarium", "Nigrospora", "Alternaria",
    "Trichoderma", "Trichoderma", "Monilinia", "Acremonium", "Penicillium",
    "Penicillium", "Nigrospora", "Epicoccum", "Epicoccum", "Trichoderma",
    "Aureobasidium", "Acremonium", "Trichoderma", "Cladosporium", "Rhizomucor",
    "Rhizopus", "Fusarium", "Hamigera", "Fusarium", "Rhizopus", "Talaromyces",
    "Hypocrea", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Rasamsonia", "Aureobasidium", "Hamigera", "Byssochlamys", "Penicilliopsis",
    "Mariannaea", "Ascospirella", "Microdochium", "Pezicula", "Penicillago",
    "Penicillium", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Penicillium", "Purpureocillium", "Penicillium", "Penicillium",
    "Penicillium", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Drechslera", "Fusarium", "Acremonium", "Hypocrea", "Fusarium",
    "Cladosporium", "Cladosporium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Penicillium", "Aspergillus", "Aspergillus", "Penicillium",
    "Penicillium", "Phoma", "Fusarium", "Rasamsonia", "Phoma", "Phoma", "Phoma",
    "Phoma", "Nigrospora", "Mariannaea", "Rasamsonia", "Thermoascus", "Hypocrea",
    "Hypocrea", "Scopulariopsis", "Monascus", "Phoma", "Stemphylium",
    "Penicillium restrictum", "Penicillium", "Penicillium", "Cladosporium",
    "Cladosporium", "Rasamsonia", "Arthrinium", "Sordaria", "Ulocladium",
    "Asteromyces", "Paecilomyces", "Paecilomyces", "Paecilomyces", "Aspergillus",
    "Aspergillus", "Aspergillus", "Aspergillus", "Aspergillus", "Penicillium",
    "Penicillium", "Penicillium", "Aspergillus", "Aspergillus", "Aspergillus",
    "Aspergillus", "Aspergillus", "Penicillium", "Aspergillus", "Penicillium",
    "Aspergillus", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Penicillium", "Penicillium", "Penicillium", "Penicillium",
    "Penicillium", "Purpureocillium", "Aspergillus", "Aspergillus", "Aspergillus",
    "Penicillium"
]


# Data for Species
species_list = [
    "Smithii", "Bilaiae", "Malodoratum", "Astellatus", "Nidulans", "Aculentus",
    "Pusillus", "Citrina", "Avellanea", "Zeae", "Nigrum", "Nigrum", "Nigrum",
    "Melangenum", "Ostracoderma", "Wotroi", "Wotroi", "Rotoruae", "Rotoruae",
    "Rotoruae", "Damascenum", "Olsonii", "Montevidensis", "Funiculosus",
    "Occultus", "Equiseti", "Tricinctum", "Oryzae", "Harzianum",
    "Atroviride", "Fructigena", "Strictum", "Ochrochloron", "Ochrochloron",
    "Oryzae", "Nigrum", "Nigrum", "Pullulans", "Alternatum",
    "Longibrachiatum", "Tenuissimum", "Pusillus", "Stolonifer", "Proliferatum",
    "Avellanea", "Foetens", "Microsporus", "Apiculatus", "Thelephoricola",
    "Ruben", "Chrysogenum", "Allii-Sativi", "Flavigenum", "Argillacea",
    "Melanogenum", "Avellanea Var. Alba", "Spectabilis", "Zonata", "Elegans",
    "Lutea", "Nivale", "Carpinea", "Kabunica", "Neojanthinellum",
    "Neojanthinellum", "Neojanthinellum", "Neojanthinellum", "Onobense",
    "Onobense", "Onobense", "Restrictum", "Restrictum", "Restrictum", "Croceum",
    "Lilacinum", "Atramentosum", "Manginii", "Citrinum", "Hordei", "Brasilianum",
    "Soppii", "Waksmanii", "Jensenii", "Acuminatum", "Sulphurea", "Tricinctum",
    "Delicatulum", "Canescens", "Canescens", "Janczewskii", "Scabrosum",
    "Scabrosum", "Flavus", "Flavus", "Janczewskii", "Krskae", "Pomorum",
    "Chlamydosporum", "Piperina", "Glomerata", "Americana", "Sorghina",
    "Pomorum", "Oryzae", "Elegans", "Eburnea", "Verrucosus", "Pulvinata",
    "Pulvinata", "Brevicaulis", "Ruber", "Epicoccina", "Vesicarium",
    "Neojanthinellum", "Steckii", "Varians", "Piperina", "Phaeospermum",
    "Fimicola", "Chartarum", "Cruciatus", "Maximus", "Maximus", "Maximus",
    "Lentulus", "Thermomutatus", "Uvarum", "Uvarum", "Uvarum", "Fagi",
    "Griseopurpureum", "Ribium", "Calidoustus", "Tubingensis", "Brasiliensis",
    "Luchuensis", "Brasiliensis", "Salamii", "Insuetus", "Polonicum",
    "Fumisynnematus", "Rubens", "Frequentans", "Antarcticum", "Piscarium",
    "Fagi", "Camponotum", "Glabrum", "Glabrum", "Arizonense", "Coprobium",
    "Corylophilum", "Griseopurpureum", "Solitum", "Caseifulvum", "Lilacinum",
    "Wentii", "Aculeatinus", "Ustus", "Velutinum"
]



# Helper function to generate and save a donut chart
def generate_donut_chart_with_legend(data, output_filename):
    df = pd.DataFrame(data, columns=["Category"])
    counts = df["Category"].value_counts()

    # Create Donut Chart
    fig, ax = plt.subplots(figsize=(30, 25))  # Increased figure size for a larger chart
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=None,  # Remove labels from the chart
        autopct=lambda p: f"{int(round(p * sum(counts) / 100))}",  # Display numeric counts
        startangle=90,
        pctdistance=0.85,
        colors=plt.cm.tab20.colors,
    )

    # Add center circle to create donut shape
    center_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig.gca().add_artist(center_circle)

    # Customize font size of numbers on the chart
    for autotext in autotexts:
        autotext.set_fontsize(16)  # Adjust font size here

    # Add a legend to the right of the chart (labels only, no counts)
    legend_labels = [f"{category}" for category in counts.index]  # Remove counts from the legend
    ax.legend(
        wedges,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),  # Adjust this to control the fixed distance
        fontsize=8,
    )

    # Save the chart
    output_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "api", "static", "images"
    )
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)
    plt.savefig(output_path, format="png", dpi=300, bbox_inches="tight")
    print(f"Chart saved to: {output_path}")
    plt.close()

# Generate and save donut charts
generate_donut_chart_with_legend(genus_list, "genus_donut_chart2.png")
generate_donut_chart_with_legend(species_list, "species_donut_chart2.png")



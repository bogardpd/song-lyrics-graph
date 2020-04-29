"""Converts a text file of song lyrics into a GraphML XML document for yEd. """

import math
import re
import sys
from lxml import etree as xml
from collections import Counter

NSMAP = {
    None: "http://graphml.graphdrawing.org/xmlns",
    'y':  "http://www.yworks.com/xml/graphml"
}

STYLES = {
    'edge': {
        'color': "#333333",
        'width': 1.0,
    },
    'node': {
        'diameter': 50.0,
        'fill': "#FFCC00",
        'stroke': {
            'color': "#FF9900",
            'width': 1.0,
        },
        'text': {
            'divisor': 5, # ratio of circle diameter to font size
            'color':   "#993300",
            'font':    "Source Sans Pro Semibold",
        },
    },
}

def diameter(freq):
    """Calculates a node diameter based on the frequency of its word."""
    return STYLES['node']['diameter'] * math.sqrt(freq)

def main(argv):
    """Generates a graph from song lyrics."""
    
    try:
        lyrics_file = argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {argv[0]} <lyrics_text_file.txt>")
    
    try:
        output_file = argv[2]
    except IndexError:
        # Use the name of the input file with a .graphml extension.
        output_file = re.sub(r"\.\w+$", ".graphml", lyrics_file)

    print(f"Processing {lyrics_file} ...")

    with open(lyrics_file) as f:
        lyrics = f.read().lower()
        # Filter out text in [brackets], and punctuation except apostrophes:
        lyrics = re.sub(r"\[.*\]|[^a-z'\s]", "", lyrics)
        lyrics = lyrics.split()

    lyric_counts = Counter(lyrics)

    # Create XML root, keys, and graph:
    root = xml.Element("graphml", nsmap=NSMAP)
    xml.SubElement(root, "key", **{
        'for': "node",
        'id': "d6",
        'yfiles.type': "nodegraphics"
    })
    xml.SubElement(root, "key", **{
        'for': "edge",
        'id': "d9",
        'yfiles.type': "edgegraphics"
    })
    graph = xml.SubElement(root, "graph", id="G", edgedefault="directed")

    # Create nodes:
    for word in sorted(set(lyrics)):
        node = xml.SubElement(graph, "node", id=word)
        d6 = xml.SubElement(node, "data", key="d6")
        circle = xml.SubElement(d6, xml.QName(NSMAP['y'], "ShapeNode"))
        xml.SubElement(circle, xml.QName(NSMAP['y'], "Geometry"), **{
            'width': str(diameter(lyric_counts[word])),
            'height': str(diameter(lyric_counts[word]))
        })
        xml.SubElement(circle, xml.QName(NSMAP['y'], "Shape"), **{
            'type': "ellipse"
        })
        xml.SubElement(circle, xml.QName(NSMAP['y'], "Fill"), **{
            'color': STYLES['node']['fill'],
            'transparent': "false"
        })
        xml.SubElement(circle, xml.QName(NSMAP['y'], "BorderStyle"), **{
            'type': "line",
            'color': STYLES['node']['stroke']['color'],
            'width': str(STYLES['node']['stroke']['width'])
        })
        label = xml.SubElement(circle, xml.QName(NSMAP['y'], "NodeLabel"), **{
            'fontSize': str(int(diameter(lyric_counts[word])
                / STYLES['node']['text']['divisor'])),
            'fontFamily': STYLES['node']['text']['font'],
            'textColor': STYLES['node']['text']['color']
        })
        label.text = word

    # Create edges:
    for index, pair in enumerate(zip(lyrics[:-1], lyrics[1:])):
        edge = xml.SubElement(graph, "edge", **{
            'id': f"e{index}",
            'source': pair[0],
            'target': pair[1]
        })
        d9 = xml.SubElement(edge, "data", key="d9")
        ple = xml.SubElement(d9, xml.QName(NSMAP['y'], "PolyLineEdge"))
        line = xml.SubElement(ple, xml.QName(NSMAP['y'], "LineStyle"), **{
            'type': "line",
            'color': STYLES['edge']['color'],
            'width': str(STYLES['edge']['width']),
        })

    # Write XML file:
    tree = xml.ElementTree(root)
    tree.write(output_file, encoding='utf-8',
        xml_declaration=True, pretty_print=True)
    print(f"Wrote graph to {output_file}")

if __name__ == "__main__":
    main(sys.argv)

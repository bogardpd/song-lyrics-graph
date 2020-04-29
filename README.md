# Song Lyrics Graph
Script to generate [yEd](https://www.yworks.com/products/yed)-flavored [GraphML](http://graphml.graphdrawing.org/) graphs from song lyrics.

The generated graph will have a node for each unique word in the lyrics, with size proportional to the frequency of that word within the lyrics. Word nodes will be connected by directed edges (arrows) indicating which words directly follow which other words.

## Usage

```bash
song_lyrics_graph.py input_file.txt [output_file.graphml]
```
`input_file.txt` should be a text document containing song lyrics. Any text in [brackets] and any punctuation other than apostrophes will be ignored.

`output_file.graphml` is a [GraphML](http://graphml.graphdrawing.org/) document designed to be opened with [yEd Graph Editor](https://www.yworks.com/products/yed). If an output file is not specified, then the output file will be the input file name with a `.graphml` extension (for example, `song_lyrics_graph.py lyrics.txt` would output to `lyrics.graphml`).

## Notes

This script does not automatically position the nodes; all the nodes will initially be in the same location. Use yEd's **Layout** menu to arrange the graph. (**Tree &rarr; Balloon** generally works pretty well for most songs, but each song is different.)
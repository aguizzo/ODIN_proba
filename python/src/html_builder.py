
def build_html(json_data):
    load_d3 = """\
<script>
    requirejs.config({
        paths: { 
            'd3': ['//cdnjs.cloudflare.com/ajax/libs/d3/4.13.0/d3.min'], 
        },                                         
    });
</script>
"""

    require_start = 'require(["d3"], function(d3) {'
    require_end = "});"

    select_svg="""\
let svg = d3.select("svg");
let width = svg.attr("width");
let height = svg.attr("height");
"""

    load_data="""\
const jsonData = {json_data};
let graphData = JSON.parse(jsonData);
""".format(json_data=json_data)
    
    physics="""\
let simulation = d3
    .forceSimulation(graphData.nodes)
    .force("charge", d3.forceManyBody().strength(-30))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force(
      "link",
      d3.forceLink(graphData.links).id((d) => d.name)
    )
    .on("tick", ticked);

let drag = d3
    .drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
"""

    links = """\
let links = svg
    .append("g")
    .selectAll("line")
    .data(graphData.links)
    .enter()
    .append("line")
    .attr("stroke-width", 3)
    .style("stroke", "orange");
"""
    nodes = """\
let textAndNodes = svg
    .append("g")
    .selectAll("g")
    .data(graphData.nodes)
    .enter()
    .append("g")
    .call(drag);

let circles = textAndNodes
    .append("circle")
    .attr("r", 5)
    .attr("fill", "red")
    .attr("id", (d) => {
      return d.name;
    });

let texts = textAndNodes.append("text").text((d) => d.name);
"""
    physics_functions="""\
function ticked() {
    textAndNodes.attr(
      "transform",
      (d) => "translate(" + d.x + ", " + d.y + ")"
    );

    links
      .attr("x1", function (d) {
        return d.source.x;
      })
      .attr("y1", function (d) {
        return d.source.y;
      })
      .attr("x2", function (d) {
        return d.target.x;
      })
      .attr("y2", function (d) {
        return d.target.y;
      });
  }

function dragstarted(d) {
    simulation.alphaTarget(0.3).restart();
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }
function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

function dragended(d) {
    simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
"""
    click_event="""\
for (const node of graphData.nodes) {
    const nodeElement = document.getElementById(node.name);
    nodeElement.addEventListener("click", function () {
      console.log(`Click on ${nodeElement.id}`);
      postToServer(nodeElement.id);
    });
  }

async function postToServer(nodeId) {
    try {
      await fetch("http://localhost:3000/click", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ event: "click", nodeId: nodeId }),
      });
    } catch (error) {
      console.error(error);
    }
  }"""

    main_script="""\
{select_svg}
{load_data}
{physics}
{links}
{nodes}
{physics_functions}
{click_event}
""".format(
        select_svg=select_svg,
        load_data=load_data,
        physics=physics,
        links=links,
        nodes=nodes,
        physics_functions=physics_functions,
        click_event=click_event
    )


    html = """\
{load_d3}
<svg width="600" height="600"></svg>

<script>
{require_start}
    {main_script}
{require_end}
</script>""".format(
        load_d3=load_d3,
        require_start=require_start,
        main_script=main_script,
        require_end=require_end
    ).strip()

    return {"text/html": html}

# json = '{"nodes": [{"name": 0}, {"name": 1}, {"name": 2}, {"name": 3}], "links": [{"source": 0, "target": 1}, {"source": 0, "target": 2}, {"source": 1, "target": 0}, {"source": 1, "target": 2}, {"source": 1, "target": 3}, {"source": 2, "target": 0}, {"source": 2, "target": 1}, {"source": 2, "target": 3}, {"source": 3, "target": 1},{"source": 3, "target": 2}]}'

# //print(build_html(json))
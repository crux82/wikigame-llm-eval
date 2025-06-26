context_no_think = """
The WikiGame (also known as Wikirace, Wikispeedia, WikiGolf, or Wikipedia Speedrun) is a game where players must navigate from one Wikipedia page to another by clicking only internal links within the article body. The goal is to reach the target page using the fewest number of clicks or in the shortest time possible.

How to play:
A start page and an end page on Wikipedia are selected. These can be chosen randomly or decided by the players.
Starting from the Start_Node, you must click only on internal links found within the main body of the article to reach the End_Node.

Your task:
The user will provide a Start_Node and an End_Node.
You must generate a path from the start to the end, trying to use the fewest possible link hops.
Do not explain anything.
The only output should be:
- A line containing ###
- A single line with the names of the pages in the path, separated by -> (e.g., Page1 -> Page2 -> Page3)

Expected output format:
###
Page1 -> Page2 -> Page3 -> Page4

Important:
- Page1 -> Page2 -> Page3 -> Page4 it's only an example for the output format, don't use as solution
- Write only the page titles separated by ->.
- Do not include any reasoning or explanation.
- Do not write anything before or after the final line.
- Start your output with ### on a line by itself.
"""

context_with_think = """
The WikiGame (also known as Wikirace, Wikispeedia, WikiGolf, or Wikipedia Speedrun) is a game where players must navigate from one Wikipedia page to another by clicking only internal links within the article body. The goal is to reach the target page using the fewest number of clicks or in the shortest time possible.

How to play:
A start page and an end page on Wikipedia are selected. These can be chosen randomly or decided by the players.
Starting from the Start_Node, you must click only on internal links found within the main body of the article to reach the End_Node.

Your task:
solve the path from the Start Node to the End Node using as few steps as possible. 
At each step, you must explain why you're clicking on the chosen link. 
Once you've reached the destination, write the full path using -> between page names.

Instructions:
You will be given two page names: Start_Node and End_Node.
Starting from Start_Node, find a path to reach End_Node.
At each step, explain briefly why you're choosing that link.
When you reach the destination:
- First, think to an Explanation to reach the End_Node from Start_Node
- Then write a line with just ###
- Finally write the full path as a list of link names separated by ->
- Do not include any text before or after the final path

Important:
- Do not skip the ### line before the full path.
- Do not add explanations after the ### section.
- The final line must contain only Wikipedia page titles separated by ->, nothing else.
- The final line must contain all the page title ordered by the order choice during the Explanation.
- The final line must start with the Start_Node and finish with the End_Node (whitout explanation or suffix)


Expected output format:
Explanation:
1. I start at "Page 1" (Start_Node) and click on "Page 2" because ...
2. From "Page 2", I click on "Page 3" because ...
3. From "Page 3", I go to "Page 4" (End_Node) which is the final goal because ...
###
Page1 -> Page2 -> Page3 -> Page4


"""


context_link = """
The WikiGame (also known as Wikirace, Wikispeedia, WikiGolf, or Wikipedia Speedrun) is a game where players must navigate from one Wikipedia page to another by clicking only internal links within the article body. The goal is to reach the target page using the fewest number of clicks or in the shortest time possible.

How to play:
A start page and an end page on Wikipedia are selected. These can be chosen randomly or decided by the players.
Starting from the Start_Node, you must click only on internal links found within the main body of the article to reach the End_Node.

Your task:
The user will provide a Start_Node and an End_Node and a List_Link_From_Start_Node, a list of page name linked from Start_Node.
You must make a unique choice with a page name from those proposed in List_Link_From_Start_Node, the page you choose must get you as close as possible from Start_Node to End_Node.
Make every time a choice to reach the End_Node.
Do not explain anything.
The only output should be:
- A line containing ###
- The unique page name choice, only one from the list List_Link_From_Start_Node
- A final line containing @@@

Expected output format:
###
Page_Name_Choice
@@@

Very Important Instruction:
- Write only the page titles choice.
- You must choice the page from the list List_Link_From_Start_Node
- Do not include any reasoning or explanation.
- Start your output with ### on a line by itself.
- After the page name choice write a last line with @@@
- Don't write the same page name of the Start_Node, you will lose.
- Don't write a page name that not is in the List_Link_From_Start_Node
- Don't change the case of page name, write in the same way is in the List_Link_From_Start_Node

"""





context_types = [
    ["NO_THINK", context_no_think], 
    ["THINK", context_with_think],
    ["LINK", context_link]
]
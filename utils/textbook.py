

template="""
Textbook Chapter:
{0}


Instruction:
Above is the content of the textbook chapter. Please read the chapter carefully and answer the following question.

"""


index_generator_template = """
first let me give you the context you need to do the following task.
1. I will give you content of a textbook first 5-10 pages.
2. you have to read the content and then generate a tree structure of the textbook as fallows.
```
    ** <chapter name> (startpage number - end page number)
        * <sub-chapter - name>  (strt page number - end page number)
        .
        .
        .
    .
    .
    .

    
Here's the textbook first 20 pages:
{0}
```

"""


class TextbookPrompt:
    def __init__(self, chapter_content):
        self.chapter_content = chapter_content
        self.question = []

    def render(self, question):
        self.question.append(question)
        return template.format(
            chapter_content=self.chapter_content,
            question=question
        )
    
import frontmatter
import markdown2


class MarkdownParser:
    def __init__(self):
        # TODO: Implement Parser options
        pass

    def parse(self, file):
        post = self.md_to_yaml(file)
        code = self.yaml_to_html(post.content)

        parsed = {'content': code.replace('\n\n', '\n')}
        for key, value in post.metadata.items():
            if key == 'content':
                raise KeyError
            parsed[key] = value

        return parsed

    def md_to_yaml(self, file):
        if not self.__is_markdown(file):
            raise ValueError

        with open(file) as f:
            data = frontmatter.loads(f.read())

        return data

    @staticmethod
    def yaml_to_html(data):
        code = markdown2.markdown(data, extras=["cuddled-lists"])
        return code

    @staticmethod
    def __is_markdown(file):
        try:
            extension = file.split('.')[1].lower()
            if not extension == 'md' and not extension == 'markdown':
                return False
            return True
        except IndexError:
            return False

import os

EXCLUDE_DIRS = ['.git', 'docs', '.vscode', '.circleci']
README_MD = ['README.md', 'readme.md', 'index.md']
COURSE_CATA = ['数学', '科学', '计算机', '语言', '技术', '其他']

TXT_EXTS = ['md', 'txt']
TXT_URL_PREFIX = 'https://github.com/ballsnow/zju-open-course/blob/master/'
BIN_URL_PREFIX = 'https://github.com/ballsnow/zju-open-course/raw/master/'


def list_files(course: str):
	filelist_texts = '## 文件列表\n\n'
	readme_path = ''
	for root, dirs, files in os.walk(course):
		level = root.replace(course, '').count(os.sep)
		indent = ' ' * 4 * level
		filelist_texts += '{}- {}\n'.format(indent, os.path.basename(root))
		subindent = ' ' * 4 * (level + 1)
		for f in files:
			if f not in README_MD:
				if f.split('.')[-1] in TXT_EXTS:
					filelist_texts += '{}- [{}]({})\n'.format(subindent,
															  f, '{}{}/{}'.format(TXT_URL_PREFIX, root,  f))
				else:
					filelist_texts += '{}- [{}]({})\n'.format(subindent,
															  f, '{}{}/{}'.format(BIN_URL_PREFIX, root,  f))
			else:
				readme_path = '{}/{}'.format(root, f)
	return filelist_texts, readme_path


def generate_md(course_path: str, filelist_texts: str, readme_path: str):
	final_texts = ['\n\n', filelist_texts]
	if readme_path:
		with open(readme_path, 'r', encoding="utf-8") as file:			
			final_texts = file.readlines() + final_texts
	with open('./docs/{}.md'.format(course_path), 'w+', encoding="utf-8") as file:
		file.writelines(final_texts)


if __name__ == '__main__':
	# scan certain course type directory 
	for course_type in COURSE_CATA:
		courses = list(filter(lambda x: os.path.isdir('./{}/{}'.format(course_type,x)), os.listdir('./'+ course_type+'/')))  # list courses
		for course in courses:
			course_path = './{}/{}'.format(course_type,course)
			filelist_texts, readme_path = list_files(course_path)
			generate_md(course_path, filelist_texts, readme_path)

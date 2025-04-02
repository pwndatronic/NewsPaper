'''1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).'''
# u1 = User.objects.create_user(username='Эдвард Титч')
# u2 = User.objects.create_user(username='Говард Лавкрафт')

'''2. Создать два объекта модели Author, связанные с пользователями.'''
# a1 = Author.objects.create(author=u1)
# a2 = Author.objects.create(author=u2)

'''3. Добавить 4 категории в модель Category.'''
# Category.objects.create(category_name='Погода')
# Category.objects.create(category_name='Политика')
# Category.objects.create(category_name='Путешествия')
# Category.objects.create(category_name='Мистика')

'''4. Добавить 2 статьи и 1 новость.'''
'''Извините, 4 добавил.'''
# post1 = Post.objects.create(post_title='Хребты Безумия', post_content='ARTC', author=a2)
# post2 = Post.objects.create(post_title='Погода на сегодня', post_content='NEWS', author=a2)
# post3 = Post.objects.create(post_title='Пособие по управлению кораблем', post_content='ARTC', author=Author.objects.get(pk=1))
# post4 = Post.objects.create(post_title='Трамп сдержал все свои обещания!', post_content='NEWS', author=a1)

'''5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).'''
# PostCategory(post=post1, category=Category.objects.get(pk=4)).save()
# PostCategory(post=post1, category=Category.objects.get(pk=3)).save()
# PostCategory(post=post2, category=Category.objects.get(pk=1)).save()
# PostCategory(post=post3, category=Category.objects.get(pk=3)).save()
# post4.categories.set(Category.objects.get(pk=2))
# post4.categories.add(Category.objects.get(pk=4))

'''Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).'''
# com1 = Comment.objects.create(comment_text='Просто невероятно!', comment_in_post=post4, comment_by_user=u2)
# com2 = Comment.objects.create(comment_text='Да я сам в шоке!', comment_in_post=post4, comment_by_user=u1)
# com3 = Comment.objects.create(comment_text='Ваше творчество переоценено, сударь!', comment_in_post=post1, comment_by_user=u1)
# com4 = Comment.objects.create(comment_text='Опять брать этот зонтик...', comment_in_post=post2, comment_by_user=u1)
# com5 = Comment.objects.create(comment_text='Невероятно! Так вот как у вас получалось грабить испанцев.', comment_in_post=post3, comment_by_user=u2)

'''7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.'''
# post1.like()
# post1.save()
# com1.like()
# com1.save()

'''8. Обновить рейтинги пользователей.'''
'''18'''
# a1.update_rating()
'''10'''
# a2.update_rating()

'''9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).'''
# best = Author.objects.order_by('-author_rating')[0]
# print(f'Лучший автор: {best.author.username}, его рейтинг: {best.author_rating}.')
# Author.objects.order_by('-author_rating').values('author__username', 'author_rating').first()

'''10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.'''
# best_post = Post.objects.order_by('-post_rating')[0]
# print(f'Дата и время добавления: {best_post.post_creation_datetime};\n'
#       f'Имя автора: {best_post.author.author.username};\n'
#       f'Рейтинг статьи: {best_post.post_rating};\n'
#       f'Заголовок: {best_post.post_title}\n'
#       f'Превью: {best_post.preview()}\n')

# Post.objects.order_by('-post_rating').values('post_creation_datetime', 'author__author__username', 'post_rating', 'post_title').first()

'''11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.'''
# coms_in_best = Comment.objects.filter(comment_in_post=best_post)
#
# for comment in coms_in_best:
#     print(f'Дата: {comment.comment_creation_datetime}\n'
#           f'Пользователь: {comment.comment_by_user.username}\n'
#           f'Рейтинг: {comment.comment_rating}\n'
#           f'Текст: {comment.comment_text}\n')

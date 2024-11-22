# Гайд по работе с bump2version, commitizen, ветками, dev и Git
1. **Клонируем репозиторий** 

   ```bash
   git clone https://github.com/your_username/telegram-bot-project.git
   ```
2. **Делаем pull. Обязательно синхронизируйтесь**

    ```bash
    git pull origin master
    ```
3. **Создаем ветку задачи. В master не пушим. Здесь ведем разработку.**
    ```bash
    git checkout -b feature0.1.1 # например, не всегда так
    ```
## semver
В основе лежит SEMVER с использованием comitizen, bump2version. Файлы конфигурации не трогаем. \
Кратко по шагам
1. Делаете свою разработку 
2. Делаете `git add .`
3. Делаете `cz commit`
    ```bash
    ? Select the type of change you are committing docs: Documentation only changes
    ? What is the scope of this change? (class or file name): (press [enter] to skip)
 
    ? Write a short and imperative summary of the code changes: (lower case and no period)
    changelog updated
    ? Provide additional contextual information about the code changes: (press [enter] to skip)
 
    ? Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer No
    ? Footer. Information about Breaking Changes and reference issues that this commit closes: (press [enter] to skip)
    ```
    На выбор в первом рассказываете, что делали, например,
    * выбираете feat (Добавление функционала)
    * выбираете docs (Добавление документации)
    * и тд
    Далее `Enter`, затем кратко описываете что делали, своими словами без излишеств (2-5 слов). Затем все `Enter`
3. Делаете `bump2version patch/minor/major` в зависимости от вида задачи
* Patch - маленькие исправления из разряда исправление бага или добавление мелкого функционала
* Minor - задача с чуть большими затратами. В основном разработка нового функицонала
* Major - глобальные изменения, которые касаются несовместых с решением задач
После этого у вас появится допустим, версия проекта `0.1.1-dev0`, затем `git push` в ветку
4. Создаете себе ветку test (см как было выше, куда отправляете merge request через github)
5. Указываете кого хотите рецензентом, ждете, пока ваш код посмотрят и дадут обратную связь
* В случае если вам надо что-то изменить менять надо не patch, minor или major, a dev
    ```bash
    bump2version dev
    ```
6. Выполняете так же merge request в тот же тест и до победного повторяете 4-5. Затем сливаете с test, тесируете у себя на локалке, отлавливаете недочеты
7. Повтор шагов 3-6 по ситуации
8. как только все проверили 
    ```bash
    bump2version release
    ```
    0.1.1-dev0 -> 0.1.1
9. Делаете обноваление истории логов

    ```bash
    cz changelog
    ```
10. В конце концов отправляете свой merge request в master, ждем слияния


# 1. Image de base
FROM node:18-alpine

# 2. Dossier de travail
WORKDIR /usr/src/app

# 3. Copie des fichiers de dépendances
COPY package*.json ./

# 4. Installation
RUN npm install

# 5. Copie du reste du code
COPY . .

# 6. Port exposé
EXPOSE 3000

# 7. Lancement
CMD ["node", "app.js"]
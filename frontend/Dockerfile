FROM node:20.10-bookworm-slim

ENV NODE_ENV=production 

# ENV VITE_BASE_API_URI_PROD="app:4173"
# ENV VITE_BASE_API_URI_DEV="0.0.0.0:5173"

WORKDIR /app

COPY package.json ./

# pnpm must be installed as it doesn't come with the default image
RUN npm i
COPY . ./

RUN npm run build
# ENV HOST is not though you can uncomment if if needed
# ENV HOST=0.0.0.0
EXPOSE 4173

CMD ["npm","run","preview" , "--host"]

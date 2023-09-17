const { Client, Collection } = require('discord.js');
const dotenv = require('dotenv'); dotenv.config();
const Logger = require("./src/utils/Logger");


const client = new Client({
  intents: 3276799,
  partials: ["MESSAGE", "CHANNEL", "REACTION", "USER", "GUILD"],
});
["commands", "buttons", "selects"].forEach(
  (x) => (client[x] = new Collection())
);

["CommandUtil", "EventUtil"].forEach(handler => { require(`./src/utils/handlers/${handler}`)(client) });

process.on("exit", (code) => {
  Logger.client(`Le processus s'est arrêté avec le code: ${code}!`);
});

process.on("uncaughtException", (err, origin) => {
  Logger.error(`UNCAUGHT_EXCEPTION: ${err}`);
  console.error(`Origine: ${origin}`);
});

process.on("unhandledRejection", (reason, promise) => {
  Logger.warn(`UNHANDLED_REJECTION: ${reason}`);
  console.log(promise);
});

process.on("warning", (...args) => Logger.warn(...args));

client.login(process.env.DISCORD_TOKEN);


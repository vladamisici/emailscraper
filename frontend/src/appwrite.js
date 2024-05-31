import { Client, Account } from "appwrite";

const client = new Client()
    .setEndpoint('https://cloud.appwrite.io/v1')
    .setProject('66560ddb000ec240d819')

const account = new Account(client)

export {account, client};
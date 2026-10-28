// Intentionally empty by default.
// Add Drizzle tables here when the site actually needs a database.
// See examples/d1/db/schema.ts for an opt-in example.
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';
export const profiles=sqliteTable('profiles',{id:text('id').primaryKey(),name:text('name').notNull(),role:text('role').notNull(),sector:text('sector').notNull(),country:text('country').notNull(),amount:integer('amount').notNull(),stage:text('stage').notNull(),bio:text('bio').notNull(),cadence:text('cadence').notNull(),status:text('status').notNull().default('pending'),paid:integer('paid').notNull().default(0),verified:integer('verified').notNull().default(0),created:text('created').notNull()});
export const connections=sqliteTable('connections',{id:text('id').primaryKey(),sender:text('sender').notNull(),recipient:text('recipient').notNull(),status:text('status').notNull().default('pending'),created:text('created').notNull()});
export const messages=sqliteTable('messages',{id:text('id').primaryKey(),connection:text('connection').notNull(),sender:text('sender').notNull(),body:text('body').notNull(),created:text('created').notNull()});
export const uploads=sqliteTable('uploads',{id:text('id').primaryKey(),owner:text('owner').notNull(),kind:text('kind').notNull(),name:text('name').notNull(),mime:text('mime').notNull()});
export const payments=sqliteTable('payments',{id:text('id').primaryKey(),owner:text('owner').notNull(),amount:integer('amount').notNull(),created:text('created').notNull()});

export const billing=sqliteTable('billing',{owner:text('owner').primaryKey(),customer:text('customer').notNull(),subscription:text('subscription').notNull()});

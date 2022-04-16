export interface TableRow {
    id: number;
    name: string;
    distance: number;
    quantity: number;
    date: string;
}

export interface IOrderingFields {
    id?: boolean,
    name?: boolean,
    distance?: boolean,
    quantity?: boolean
}
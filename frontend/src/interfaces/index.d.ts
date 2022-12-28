export interface IPortfolio {
    id: number;
    name: string;
    broker?: IBroker
    broker_id?: string;
    brokerId?: string;
}

export interface IBroker {
    id: string;
    name: string;
}
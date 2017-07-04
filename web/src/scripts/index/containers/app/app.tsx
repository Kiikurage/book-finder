import AppBar from "material-ui/AppBar";
import { Card, CardActions, CardText } from "material-ui/Card";
import FlatButton from "material-ui/FlatButton";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import SearchIcon from "material-ui/svg-icons/action/search";
import TextField from "material-ui/TextField";
import * as React from "react";
import "./app.scss";

interface Props extends React.ClassAttributes<HTMLDivElement> {
}

interface State {
    json: ({ title: string, image: string })[]
}

class App extends React.Component<Props, State> {
    constructor() {
        super();
        this.state = {
            json: []
        };
    }

    onItemClick(item: { title: string, image: string }) {
        this.findBook(item.image)
    }

    onSearchButtonTapped() {
        this.searchImages();
    }

    async findBook(imageUrl: string) {
        let data = new FormData();
        data.append('imageUrl', imageUrl);

        let res = await fetch('/api/find', {
            method: 'POST',
            body: data
        });

        let json = await res.json();
        console.log(json);
    }

    async searchImages() {
        let queryField = this.refs['query'] as TextField;
        let query = queryField.getValue().trim();
        if (query == '') return;

        this.setState({
            json: []
        });
        let res = await fetch('/api/search', {
            method: 'POST',
            body: JSON.stringify({'q': query}),
            headers: {'Content-Type': 'application/json'}
        });

        let json = await res.json();
        this.setState({
            json: json
        });
    }

    render() {
        let items = this.state.json.map((data: { title: string, image: string }, i: number) => {
            return (<li key={i} onClick={() => this.onItemClick(data)}>
                <img width="128" height="128" src={data.image}/>
                <span>{data.title}</span>
            </li>);
        });

        return (<MuiThemeProvider>
            <div className="App">
                <AppBar className="App-Header" iconStyleLeft={{
                    display: 'none',
                }} title="Book Finder"/>
                <main className="App-Main">
                    <Card>
                        <CardText>
                            <TextField ref="query"
                                       style={{
                                           width: '100%',
                                           textAlign: 'center'
                                       }}
                                       floatingLabelText="書籍名"
                                       floatingLabelFixed={true}
                                       hintText="検索したい書籍名の一部を入力"/>
                        </CardText>
                        <CardActions>
                            <FlatButton style={{width: '100%'}} label="検索" icon={<SearchIcon />}
                                        onClick={() => this.onSearchButtonTapped()}/>
                        </CardActions>
                    </Card>
                    <ul style={{
                        flex: '1 1',
                        overflow: 'auto',
                    }}>
                        {items}
                    </ul>
                </main>
            </div>
        </MuiThemeProvider>);
    }
}

export default App;
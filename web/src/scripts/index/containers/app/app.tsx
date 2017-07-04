import * as classNames from "classnames";
import AppBar from "material-ui/AppBar";
import { Card, CardActions, CardText } from "material-ui/Card";
import FlatButton from "material-ui/FlatButton";
import RaisedButton from "material-ui/RaisedButton";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";
import SearchIcon from "material-ui/svg-icons/action/search";
import TextField from "material-ui/TextField";
import * as React from "react";
import "./app.scss";

interface Props extends React.ClassAttributes<HTMLDivElement> {
}

interface State {
    json: ({ title: string, image: string })[],
    activeView: ViewID,
    bookImageUrl: string | null,
    targetImage: File | null
    resultImage: Blob | null
}

enum ViewID {
    SearchView = 0,
    PhotoView
}
class App extends React.Component<Props, State> {
    constructor() {
        super();
        this.state = {
            json: [],
            activeView: ViewID.SearchView,
            bookImageUrl: null,
            targetImage: null,
            resultImage: null
        };
    }

    onItemClick(item: { title: string, image: string }) {
        this.setState({
            bookImageUrl: item.image
        });
        this.activatePhotoView();
    }

    onSearchButtonTapped() {
        this.searchImages();
    }

    async onUploadPhotoButtonClick() {
        let img = await new Promise<File>((resolve, reject) => {
            let $input = document.createElement('input');
            $input.type = 'file';
            $input.multiple = false;
            $input.accept = 'image/*';
            $input.style.visibility = 'hidden';
            $input.style.position = 'absolute';
            document.body.appendChild($input);

            $input.onchange = async () => {
                document.body.removeChild($input);
                resolve($input.files![0]);
            };

            $input.click();
        });

        this.setState({
            targetImage: img
        });
        this.findBook();
    }

    activatePhotoView() {
        this.setState({
            activeView: ViewID.PhotoView
        });
    }

    async findBook() {
        let targetImage = this.state.targetImage!;
        let data = new FormData();

        data.append('bookImageUrl', this.state.bookImageUrl!);
        data.append('targetImage', targetImage);

        let resultImage = await (await fetch('/api/find', {
            method: 'POST',
            body: data
        })).blob();

        this.setState({
            resultImage: resultImage
        });
    }

    async searchImages() {
        let queryField = this.refs['query'] as TextField;
        let query = queryField.getValue().trim();
        if (query == '') return;

        this.setState({
            json: [],
            targetImage: null,
            resultImage: null
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
                    <section className="App-SearchView">
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
                    </section>
                    <section className={classNames('App-PhotoView', {
                        'App-PhotoView-Show': this.state.activeView == ViewID.PhotoView
                    })}>
                        {this.state.resultImage ?
                            <img style={{maxWidth: '100%', margin: '16px'}}
                                 src={URL.createObjectURL(this.state.resultImage)}/> :
                            this.state.targetImage ?
                                <img style={{maxWidth: '100%', margin: '16px'}}
                                     src={URL.createObjectURL(this.state.targetImage)}/> :
                                null}
                        <span>
                            {this.state.resultImage ?
                                '多分この辺' :
                                this.state.targetImage ?
                                    '本を検索中...' :
                                    null}
                        </span>
                        <RaisedButton primary label="画像をアップロード"
                                      onClick={() => this.onUploadPhotoButtonClick()}/>
                    </section>
                </main>
            </div>
        </MuiThemeProvider>);
    }
}

export default App;
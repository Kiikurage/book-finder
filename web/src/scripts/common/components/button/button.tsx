import * as classNames from "classnames";
import * as React from "react";
import "./button.scss";

interface Props extends React.HTMLAttributes<HTMLButtonElement> {
    icon?: React.ReactNode,
    srcSet?: string,
    primary?: boolean
    active?: boolean
}

interface State {
}

export class Button extends React.Component<Props, State> {
    constructor() {
        super();

        this.state = {}
    }

    render() {
        let img: React.ReactNode = this.props.icon;
        if (typeof img == 'string') {
            img = <img className="Button-Image"
                       src={img}
                       srcSet={this.props.srcSet}/>
        }

        return (
            <button className={classNames('Button', this.props.className, {
                'Button--active': this.props.active,
                'Button--primary': this.props.primary
            })}
                    disabled={this.props.disabled}
                    onClick={this.props.onClick}>
                {img}
                <div className="Button-Body">{this.props.children}</div>
            </button>
        );
    }
}
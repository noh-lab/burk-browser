define([
           'dojo/_base/declare',
           'dojo/dom-construct',

           'dijit/Toolbar',
           'dijit/form/Button',
           'JBrowse/Util',
           'JBrowse/has'
       ],
       function( declare, dom, Toolbar, Button, Util, has ) {


return declare(null,
{

    constructor: function( args ) {

        if (typeof args === 'undefined') {
            this.width = 78;
            return;
        };

        this.width       = args.width || 78;
        this.htmlMaxRows = args.htmlMaxRows || 15;
        this.track = args.track;
        this.canSaveFiles = args.track &&  args.track._canSaveFiles && args.track._canSaveFiles();

    // hook point
    if (typeof this.initData === 'function')
        this.initData(args);
    },
    renderHTML: function( region, seq, parent ) {
        var thisB = this;
        var text = this.renderText( region, seq );
        var lineCount = text.match( /\n/g ).length + 1;
        var container = dom.create('div', { className: 'aminoacidView' }, parent );

        if( this.canSaveFiles ) {
            var toolbar = new Toolbar().placeAt( container );
            var thisB = this;

        // hook point
    if (typeof thisB.addButtons === 'function')
            thisB.addButtons(region, seq, toolbar);

            toolbar.addChild( new Button(
                                  { iconClass: 'dijitIconSave',
                                    label: 'Amino Acid',
                                    title: 'save as FAA',
                                    disabled: ! has('save-generated-files'),
                                    onClick: function() {
                                        thisB.track._fileDownload(
                                            { format: 'FAA',
                                              filename: Util.assembleLocString(region)+'.faa',
                                              data: text
                                            });
                                    }
                                  }));
        }

        var textArea = dom.create('textarea', {
                        className: 'faa',
                        cols: this.width,
                        rows: Math.min( lineCount, this.htmlMaxRows ),
                        readonly: true
                    }, container );
        var c = 0;
        textArea.innerHTML = text.replace(/\n/g, function() { return c++ ? '' : "\n"; });
        return container;
    },
    /**
     * returns faa formatted string
     * @param {f object} region - faa formated text string
     * @param {string} seq - unformated sequence
     * @returns {String} - faa formated string
     */
    renderText: function( region, seq ) {
        return '>' + region.product
            + '\n'
            + this._wrap( this.proteinFromNuc( seq ), this.width );
    },
    proteinFromNuc: function( seq ) {
        var splitSeq = seq.match(/.{1,3}/g)
        var protSeq = splitSeq.map(Util.codonMapping)
        return protSeq.join('');;
    },
    _wrap: function( string, length ) {
        length = length || this.width;
        return string.replace( new RegExp('(.{'+length+'})','g'), "$1\n" );
    }
});
});
